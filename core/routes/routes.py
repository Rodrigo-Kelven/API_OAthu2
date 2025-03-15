from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks
from core.schemas.schemas import Token, User, UserResponse, UserResponseCreate, UserResponseEdit
from core.config.config_db import  get_db_users
from core.models.models import UserDB
from typing import List, Annotated
from core.auth.auth import *

from core.services.service import ServicesAuth


# caso queira entender como funciona, recomendo desenhar o fluxo
routes_auth_auten = APIRouter()



# rota login, esta rota recebe os dados do front para a validacao
@routes_auth_auten.post(
        path="/login",
        status_code=status.HTTP_202_ACCEPTED,
        response_description="Informations of login",
        description="Route login user",
        name="Route login user"
)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    return ServicesAuth.login_user(form_data)



# rota para ter suas informacoes
@routes_auth_auten.get(
        path="/users/me/",
        status_code=status.HTTP_200_OK,
        response_model=UserResponse,
        response_description="Informations user",
        description="Route get informations user",
        name="Route get informations user"
)
async def read_users_me(current_user: Annotated[User , Depends(get_current_active_user)]):
    
    return ServicesAuth.read_users_informations(current_user)



# rota para ter as informacoes sobre seus items, lembre da alura, aqui seria onde guarda os "certificados"
@routes_auth_auten.get(
        path="/users/me/items/",
        status_code=status.HTTP_200_OK,
        response_description="Informations items user",
        description="Route get items user",
        name="Route get items user"
)
async def read_own_items(current_user: Annotated[User , Depends(get_current_active_user)]):
    
    return [{"item_id": "Foo", "owner": current_user.username}]



# Rota para criar um novo usuário -> qualquer usuario pode criar 
@routes_auth_auten.post(
        path="/users/",
        status_code=status.HTTP_201_CREATED,
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
    db: Session = Depends(get_db_users)
):
    return ServicesAuth.create_user(username, email, full_name, password,db)



# Listar todos os usuários -> somente user admin 
@routes_auth_auten.get(
        path="/users/",
        status_code=status.HTTP_200_OK,
        response_model=List[UserResponse],
        response_description="Users",
        description="Route list users",
        name="Route list users"
)
async def get_users(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
    
    return ServicesAuth.get_all_users(current_user)


# Atualizar informações do usuário
@routes_auth_auten.put(
        path="/users/{username}",
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse,
        response_description="Update informations user",
        description="Route update informations user",
        name="Route informations user"
)
async def update_user(username: str, user: UserResponseEdit, current_user: Annotated[User , Depends(get_current_active_user)]):

    return ServicesAuth.update_user(username, user, current_user)


# Deletar a conta do usuário somente autenticado
@routes_auth_auten.delete(
        path="/users/delete-account-me/",
        status_code=status.HTTP_202_ACCEPTED,
        response_description="Informations delete account",
        name="Route delete user"
)
async def delete_user(current_user: Annotated[User , Depends(get_current_active_user)]):

    return ServicesAuth.delete_user(current_user)


# exemplo simples sistena de envio de mensagem por email
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@routes_auth_auten.post(
        "/send-notification/email",
        status_code=status.HTTP_200_OK,
        response_description="Send mesage email",
        description="Route send mesage email",
        name="Route send mesage email"
)
async def send_notification(background_tasks: BackgroundTasks, email = Form(...,description="Email",title="Email")):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}