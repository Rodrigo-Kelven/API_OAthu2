from core.models.models import UserDB
from core.config.config_db import  SessionLocal
from core.config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context, oauth2_scheme
from core.schemas.schemas import Token, TokenData, User, UserResponse, UserResponseCreate
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import List, Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

# caso queira entender como funciona, recomendo desenhar o fluxo
routes_auth_auten = APIRouter()



# Funções utilitárias
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# pegar o password transformado em hash
def get_password_hash(password):
    return pwd_context.hash(password)

# pegar a sessao do primeiro usuario encontrado
def get_user(db: Session, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()


# verifica se esta autenticado
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# criar token de acesso
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# pegar a sessao atual
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db = SessionLocal()
    user = get_user(db, token_data.username)
    db.close()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User , Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@routes_auth_auten.post(
        path="/login",
        response_description="Informations of login",
        description="Route login user",
        name="Route login user"
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    db = SessionLocal()
    user = authenticate_user(db, form_data.username, form_data.password)
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# rota para ter suas informacoes
@routes_auth_auten.get(
        path="/users/me/",
        response_model=UserResponse,
        response_description="Informations user",
        description="Route get informations user",
        name="Route get informations user"
)
async def read_users_me(
    current_user: Annotated[User , Depends(get_current_active_user)],
):
    return current_user


# rota para ter as informacoes sobre seus items, lembre da alura, aqui seria onde guarda os "certificados"
@routes_auth_auten.get(
        path="/users/me/items/",
        response_description="Informations items user",
        description="Route get items user",
        name="Route get items user"
)
async def read_own_items(
    current_user: Annotated[User , Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]



# Rota para criar um novo usuário -> qualquer usuario pode criar 
@routes_auth_auten.post(
        path="/users/",
        response_model=UserResponseCreate,
        response_description="Create user",
        description="Route create user",
        name="Route create user"
)
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)

):
    db = SessionLocal()
    if get_user(db, username):
        db.close()
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password)
    db_user = UserDB(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


"""
# Listar todos os usuários sem verificacao de identificacao -> roles
@routes_auth_auten.get("/users/", response_model=List[User ], deprecated=True)
async def get_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return [User (**user.__dict__) for user in users]

"""

# Listar todos os usuários
@routes_auth_auten.get(
        path="/users/",
        response_model=List[UserResponse],
        response_description="Users",
        description="Route list users",
        name="Route list users"
)
async def get_users(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
    # Verifica se o usuário atual tem o papel de admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted")

    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return [UserResponse (**user.__dict__) for user in users]


# Atualizar informações do usuário
@routes_auth_auten.put(
        path="/users/{username}",
        response_model=UserResponse,
        response_description="Update informations user",
        description="Route update informations user",
        name="Route informations user"
)
async def update_user(
    username: str, user: UserResponse, current_user: Annotated[User , Depends(get_current_active_user)]
):
    db = SessionLocal()
    db_user = get_user(db, username)
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User  not found")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


# Deletar a conta do usuário somente autenticado
@routes_auth_auten.delete(
        path="/users/delete-account-me/",
        response_description="Informations delete account"
)
async def delete_user(current_user: Annotated[User , Depends(get_current_active_user)]):
    db = SessionLocal()
    db_user = get_user(db, current_user.username)  # Obtém o usuário autenticado
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User  not found")
    
    db.delete(db_user)
    db.commit()
    db.close()
    return {"detail": f"User  {current_user.username} deleted successfully"}
