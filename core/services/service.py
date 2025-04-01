from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks, Body
from fastapi.security import OAuth2PasswordRequestForm
from core.schemas.schemas import Token, User, UserResponse, UserResponseCreate, UserResponseEdit
from core.config.config_db import  get_db_users
from core.models.models import UserDB, Role
from typing import List, Annotated
from core.auth.auth import *


# servico somente de usuario
class ServicesAuth:

    @staticmethod
    def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

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
            data={"sub": user.username, "role": user.role}, 
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    

    @staticmethod
    def read_users_informations(current_user: Annotated[User , Depends(get_current_active_user)]):
        # Verifique as permissões antes de retornar as informações do usuário
        check_permissions(current_user, Role.user)  # Aqui verificamos se o usuário tem o papel de 'user'

        # Se a permissão foi verificada com sucesso, retornamos os dados do usuário
        return current_user
    

    @staticmethod
    def create_user(username: str = Form(...),email: str = Form(...),full_name: str = Form(...),password: str = Form(...), db: Session = Depends(get_db_users)):
         # Verifica se o username já está registrado
        if get_user(db, username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username ja registrado!")
        
        # Verifica se o email já está registrado
        if db.query(UserDB).filter(UserDB.email == email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ja registrado!")

        hashed_password = get_password_hash(password)
        db_user = UserDB(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return db_user
    

    @staticmethod
    def get_all_users(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
        # Verifique as permissões antes de retornar as informações do usuário
        check_permissions(current_user, Role.admin)  # Aqui verificamos se o usuário tem o papel de 'user'

        db = SessionLocal()
        users = db.query(UserDB).all()
        db.close()
        return [UserResponse (**user.__dict__) for user in users]
    

    @staticmethod
    def update_user(username: str, user: UserResponseEdit, current_user: Annotated[User , Depends(get_current_active_user)]):
        db = SessionLocal()
        db_user = get_user(db, username)

        if not db_user:
            db.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado!")
        
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        db.close()
        return db_user
    

    @staticmethod
    def delete_user(current_user: Annotated[User , Depends(get_current_active_user)]):
        db = SessionLocal()
        db_user = get_user(db, current_user.username)  # Obtém o usuário autenticado

        if not db_user:
            db.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado!")
        
        db.delete(db_user)
        db.commit()
        db.close()
        return {"detail": f"User  {current_user.username} deleted successfully"}