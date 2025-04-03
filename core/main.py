from core.config.config_db import Base, engine
from core.routes.all_routes import all_routes
from fastapi import FastAPI
from core.auth.auth import *
from core.config.config import *


description = """
### Api OAThu2, esta em fase de desenvolvimento
### Se sinta a vontade para compartilhar feedbacks. 🚀
"""

app = FastAPI(
    title="Simple API OAthu2",
    description=description,
    version="0.10.6"
)

# funcao para pegar todas as rotas ao inicializar
all_routes(app)

# tem que ficar no main.py, porque ao ser iniciado, as tabelas no db seram criadas imediatamente
print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas.")


# Adiciona o middleware ao FastAPI
app.add_middleware(LogRequestMiddleware)

# Adiciona o middleware de tratamento de exceções
app.add_middleware(ExceptionHandlingMiddleware)

config_CORS(app)