# Importações necessárias
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth, database
from fastapi import APIRouter

# Configurações de autenticação
SECRET_KEY = "sua_chave"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 



# Define o esquema OAuth2 para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Para rotas de autenticação
routerAuthentication = APIRouter(prefix="/auth", tags=["Authentication"])

# Função para criar um token JWT de acesso
def criar_token_acesso(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para obter o usuário atual a partir do token JWT
def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credenciais_invalidas
    except JWTError:
        raise credenciais_invalidas
    usuario = crud.get_usuario_por_username(db, username)
    if usuario is None:
        raise credenciais_invalidas
    return usuario

# Rota protegida que retorna uma mensagem se o usuário estiver autenticado
@routerAuthentication.get("")
def quem_esta_autenticado(usuario = Depends(obter_usuario_atual)):
    return {"message": f"Olá, {usuario.username}. Você está autenticado!"}


