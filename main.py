# Importações necessárias
import routes.books as books
import routes.health as health
from fastapi import APIRouter, Request
from core import auth, crud, database, models, schemas
# Importação necessárias
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core import auth, crud, database, models, schemas
from logger import setup_logger
import logging

# Inicializa o sistema de logging com o formato e configurações definidos na função setup_logger
setup_logger()
logger = logging.getLogger(__name__) # Cria um logger

# FastAPI
app = FastAPI(
    title = "Tech Challenge - API",
    version = "1.0.0",
    description = "API para consultar dados do site Books to Scrape usando Scraping - Tech Challenge",
    contact = {
        "name": "Wesley Rodrigues dos santos",
        "url": "https://www.linkedin.com"   
    }
)

# Cria todas as tabelas no banco de dados com base nos modelos definidos
models.Base.metadata.create_all(bind=database.engine)


# Middleware para registrar logs de todas as requisições HTTP
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Nova requisição", extra={
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host
    })
    response = await call_next(request)
    logger.info("Resposta enviada", extra={
        "status_code": response.status_code
    })
    return response

# Rota para criar um novo usuário
@app.post("/usuarios/", response_model=schemas.UsuarioOut, tags=["Authentication"])
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # Verifica se o usuário já existe no banco de dados
    db_usuario = crud.get_usuario_por_username(db, usuario.username)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return crud.criar_usuario(db, usuario)

# Rota para gerar token de acesso (login)
@app.post("/token", response_model=schemas.Token, tags=["Authentication"])
def Gerar_Token_com_login_criado(form_data: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):
    # Busca o usuário pelo username informado no formulário
    usuario = crud.get_usuario_por_username(db, form_data.username)
    # Verifica se o usuário existe e se a senha está correta
    if not usuario or not crud.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    access_token = auth.criar_token_acesso(data={"sub": usuario.username})
    # Retorna o token e o tipo
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para obter os dados do usuário autenticado
@app.get("/Usuario", response_model=schemas.UsuarioOut, tags=["Authentication"])
def ler_usuario_atual_apresentando_id_e_username(usuario = Depends(auth.obter_usuario_atual)):
    # Retorna os dados do usuário atual (id e username)
    return usuario


# Inclui os módulos de rota
app.include_router(books.router)
app.include_router(books.router2)
app.include_router(health.router)
app.include_router(auth.routerAuthentication)

