# Importações necessárias
from fastapi import APIRouter, Depends
import httpx


# Cria um roteador com o prefixo "/api/v1" para organizar as rotas da aplicação
router = APIRouter(prefix="/api/v1")

# • GET /api/v1/health: verifica status da API e conectividade com os dados.
@router.get("/health", tags=["Endpoints Principais"])
async def Status_da_API_e_Conectividade_com_os_dados():  
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://books.toscrape.com/")
        if response.status_code == 200:
            return {
                "status": "ok",
                "mensagem": "API está funcionando e conectada ao site Books to Scrape.",
                "site_status": response.status_code
            }
        else:
            return {
                "status": "erro",
                "mensagem": "API está ativa, mas o site Books to Scrape não respondeu corretamente.",
                "site_status": response.status_code
            }
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"API está ativa, mas ocorreu um erro ao acessar os dados: {str(e)}"
        }
