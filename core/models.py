# Importações necessárias
from sqlalchemy import Column, Integer, String
from .database import Base

# Define o modelo de dados para a tabela "usuarios"
class Usuario(Base):
    __tablename__ = "usuarios" # Nome da tabela no banco de dados
        # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True) # Id Único do usuário
    username = Column(String, unique=True, index=True) # Nome do usuário único
    senha_hash = Column(String) # Senha armazenada de forma segura(hash)
