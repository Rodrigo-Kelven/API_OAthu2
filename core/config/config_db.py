from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///./banco_de_dados.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()