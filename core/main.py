from fastapi import FastAPI
from core.config.config_db import Base, engine
from core.routes.all_routes import all_routes
from core.auth.auth import *
from fastapi.middleware.cors import CORSMiddleware


description = """
## Api OAThu2, em fase de desenvolvimento
### Se sinta a vontade para compartilhar feedbacks. 🚀

## Propósito

- Ser capaz de se implementar de forma segura e flexivel proporcionando **segurança**.

## Tópics

### Basic implementation:

* **Create users** (_implemented_).
* **Read users** (_implemented_).
* **Validate users**  (_implemented_).
* **Update criptografia** (_not implemented_).
* **Update performance** (_not implemented_).
* **Update security** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,

    version="0.0.1",
    contact={
        "name": "Rodrigo Kelven",
        "url": "http://api-auth-auten/",
        "email": "t3tese@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

all_routes(app)

# tem que ficar no main.py, porque ao ser iniciado, as tabelas no db seram criadas imediatamente
print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas.")


# Adiciona o middleware ao FastAPI
app.add_middleware(LogRequestMiddleware)

# Adiciona o middleware de tratamento de exceções
app.add_middleware(ExceptionHandlingMiddleware)


# paths onde o front ira enviar dados para o backend
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)