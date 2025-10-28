# Importações necessárias

# Importa a classe BaseModel do Pydantic, usada para validação e serialização de dados
from pydantic import BaseModel

# Modelo de entrada para criação de um novo usuário
class UsuarioCreate(BaseModel):
    username: str  # Nome de usuário fornecido pelo cliente
    senha: str     # Senha fornecida pelo cliente
# Modelo de saída para retornar dados do usuário (sem a senha)
class UsuarioOut(BaseModel):
    id: int        # ID do usuário no banco de dados
    username: str  # Nome de usuário

    class Config:
        # Permite que o Pydantic converta automaticamente objetos ORM (como do SQLAlchemy) para esse schema
        from_attributes = True

# Modelo de resposta para o token de autenticação
class Token(BaseModel):
    access_token: str  # Token JWT gerado após autenticação
    token_type: str    # Tipo do token (geralmente "bearer")

