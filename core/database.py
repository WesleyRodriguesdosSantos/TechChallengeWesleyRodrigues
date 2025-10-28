# Importações necessárias
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios.db"

# Criando o mecanismo de conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a base declarativa
Base = declarative_base()

# Função geradora que fornece uma sessão de banco de dados para uso em dependências do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

