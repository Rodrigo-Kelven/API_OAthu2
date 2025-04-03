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
    def loginUserService(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        """
        Args:
            token para a realizacao da autenticacao
        Returns:
            confirmacao do token de acesso
        Raises:
            none 'implementar tratamento' 
        """

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
    def readUsersInformationsService(current_user: Annotated[User , Depends(get_current_active_user)]):
        """
        Args:
            confirma se o token é valido, sendo valido, realiza a busca dos dados do usuario referente ao token
        Returns:
            retorna os dados do usuario caso seja validade como logado tendo o token válido
        Raises:
            caso o nao seja autorizado, recebe um erro de acesso negado. 401
        """
        # Verifique as permissões antes de retornar as informações do usuário
        check_permissions(current_user, Role.user)  # Aqui verificamos se o usuário tem o papel de 'user'

        # Se a permissão foi verificada com sucesso, retornamos os dados do usuário
        return current_user
    

    @staticmethod
    def createUserService(
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db_users)
        ):
        """
        Args:
            dados inseridos pelo usuario, e criacao do token
        Return:
            token do usuario com as informacoes passadas
        Raises:
            caso o usuario ja exista, um erro sobre é retornado
        """

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
    

    # isto sera desativado, esta funcionalidade existira no painel de admin
    @staticmethod
    def getAllUsersService(current_user: Annotated[UserResponse , Depends(get_current_active_user)]):
        """
        Args:
            recebe o token do usuario e verifica se é valido
        Return:
            caso o token inserido seja validado, o usuario tendo permissao, os dados sao retornados
        Raises:
            caso o usuario nao tenha a permissao nescessaria, um erro de acesso negado é retornado, 401
        """
        # Verifique as permissões antes de retornar as informações do usuário
        check_permissions(current_user, Role.admin)  # Aqui verificamos se o usuário tem o papel de 'user'

        db = SessionLocal()
        users = db.query(UserDB).all()
        db.close()
        return [UserResponse (**user.__dict__) for user in users]
    

    @staticmethod
    def updateUserService(
        username: str,
        user: UserResponseEdit,
        current_user: Annotated[User , Depends(get_current_active_user)]
        ):
        """
        Args:
            recebe o token como parametro para realizar o update nso dados do usuario
        Return:
            caso o token seja valido, a permissao para update dos dados é concedida
        Raises:
            caso o usuario nao tenha a permissao nescessaria, um erro de acesso negado é retornado, 401
        """
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
    def deleteUserService(current_user: Annotated[User , Depends(get_current_active_user)]):
        """
        Args:
            realiza o delete do usuairo com base no token fornecido sendo validado
        Return:
            caso o token seja valido, um erro 204 é retornado, dizendo que o usuario foi deletado
        Raises:
            caso o token do usuario nao seja valido, é retornadp um erro de acesso negado, 40
        """
        db = SessionLocal()
        db_user = get_user(db, current_user.username)  # Obtém o usuário autenticado

        if not db_user:
            db.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado!")
        
        db.delete(db_user)
        db.commit()
        db.close()
        return {"detail": f"User  {current_user.username} deleted successfully"}