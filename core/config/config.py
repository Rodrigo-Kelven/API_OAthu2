from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logging.handlers import RotatingFileHandler
import logging
import os
from slowapi import Limiter
from slowapi.util import get_remote_address


# Configurações e chave secreta

# Use este comando para gerar sua chave caso queira: openssl rand -hex 64
# sim esta chave é uma chave inutilizavel
# NÃO PODE SUBIR SUAS CHAVES PRIVADAS PARA O REPOSITORIO!!
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256" # algoritmo para a criptografia dos passwords
ACCESS_TOKEN_EXPIRE_MINUTES = 15 # tempo de expiracao do token

# Inicialização de FastAPI e outras configurações
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# O usuário digita o username e a senha no frontend e aperta Enter.
# O frontend (rodando no browser do usuário) manda o username e a senha para uma URL específica na sua API (declarada com tokenUrl="token").
# Esse parâmetro contém a URL que o client (o frontend rodando no browser do usuário) vai usar para mandar o username e senha para obter um token
# se mudar a rota de login, nao esqueca de mudar aqui, porque o fastapi simplesmente nao AVISA PORRA
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api-auten_auth/login") 

# caso precise de mais configuracao, documente e especifique porque
def config_CORS(app):
    from fastapi.middleware.cors import CORSMiddleware

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost:5173/", # react
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["X-Custom-Header"],
        max_age=3600,
    )


"""
### Resumo visual
### Nível configurado	Logs que ele aceita
-----------------------------------------------
* DEBUG	    DEBUG, INFO, WARNING, ERROR, CRITICAL
* INFO	    INFO, WARNING, ERROR, CRITICAL
* WARNING	WARNING, ERROR, CRITICAL
* ERROR	    ERROR, CRITICAL
* CRITICAL	CRITICAL
"""



os.makedirs("logs", exist_ok=True)
# Formato padrão
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Cria e retorna um logger com arquivo próprio."""
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False  # Evita que os logs se repitam no console

    return logger

# Loggers separados
app_logger = setup_logger("app_logger", "logs/app.log", logging.INFO)
auth_logger = setup_logger("auth_logger", "logs/auth.log", logging.INFO)
#db_logger = setup_logger("db_logger", "logs/db.log", logging.ERROR)
db_logger = setup_logger("db_logger", "logs/db.log", logging.INFO)



# Configurar o log de Request e Response
logging.basicConfig(level=logging.INFO)


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Requisição recebida: {request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Resposta enviada com status {response.status_code}")
        return response

# decoracor do rate limit de auth
limiter = Limiter(
    key_func=get_remote_address,
    enabled=True,
    )
