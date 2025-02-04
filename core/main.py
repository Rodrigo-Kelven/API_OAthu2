from fastapi import FastAPI
from core.config.config_db import Base, engine
from core.routes.all_routes import all_routes


app = FastAPI()
all_routes(app)

# tem que ficar no main.py, porque ao ser iniciado, as tabelas no db seram criadas imediatamente
print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas.")