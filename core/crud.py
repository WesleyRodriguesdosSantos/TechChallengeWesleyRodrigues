# Importações necessárias
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import schemas  , models

# Define o contexto de criptografia usando o algoritm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para buscar um usuário no banco de dados pelo username
def get_usuario_por_username(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()

# Função para criar um novo usuário no banco de dados
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    senha_hash = pwd_context.hash(usuario.senha)
    db_usuario = models.Usuario(username=usuario.username, senha_hash=senha_hash)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
# Função para verificar se a senha fornecida corresponde ao hash armazenado
def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)
