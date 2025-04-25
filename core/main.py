from core.config.config_db import Base_auth, engine_auth
from core.routes.all_routes import all_routes
from fastapi import FastAPI
from core.auth.auth import ExceptionHandlingMiddleware
from core.config.config import LogRequestMiddleware, config_CORS, db_logger


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

@app.on_event("startup")
async def startup_event():
    try:
        # Criação das tabelas no banco de dados de usuários
        async with engine_auth.begin() as conn:
            await conn.run_sync(Base_auth.metadata.create_all)
            db_logger.info("Tabela UserDB criada com sucesso.")

    except Exception as e:
        db_logger.error(f"Erro ao criar tabelas: {str(e)}.")


@app.on_event("shutdown")
async def shutdown_event():
    await engine_auth.dispose()
    db_logger.info("Conexões com os bancos de dados encerradas.")

# Adiciona o middleware ao FastAPI
app.add_middleware(LogRequestMiddleware)

# Adiciona o middleware de tratamento de exceções
app.add_middleware(ExceptionHandlingMiddleware)

config_CORS(app)