# Importações necessárias
import re
import requests
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from bs4 import BeautifulSoup
import httpx
import asyncio   
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import  schemas, crud, auth, database

 # Inclui os módulos de rota
router = APIRouter(prefix="/api/v1/books")
router2 = APIRouter(prefix="/api/v1/starts")
routerAuthentication = APIRouter(prefix="/auth")


# Endpoints Obrigatórios da API 

# Parseando o conteúdo HTML
pagina_books = requests.get("https://books.toscrape.com/")
dados_books = BeautifulSoup(pagina_books.text, 'html.parser') 

# Lista todos os livros disponíveis na base de dados. 
@router.get("/", tags=["Endpoints Principais"])
async def Lista_todos_os_livros_disponiveis(usuario = Depends(auth.obter_usuario_atual)):
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    livros = []
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            url = base_url.format(page)
            response = await client.get(url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            titulos = soup.find_all('h3')
            if not titulos:
                break  

            for titulo in titulos:
                livro = titulo.find('a')['title']
                livros.append(livro)

            page += 1

    return {"livros": livros}

# Retorna detalhes completos de um livro específico pelo ID. 
BASE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BOOK_BASE_URL = "https://books.toscrape.com/catalogue/"

@router.get("/id" , tags=["Endpoints Principais"] )
async def Retorna_detalhes_completos_de_um_livro_específico_pelo_ID(id: int):
    # Varre as páginas do catálogo para encontrar o slug com o ID
    for page_num in range(1, 51):  # Limitando a páginas
        page_url = BASE_CATALOGUE_URL.format(page_num)
        response = requests.get(page_url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            link_tag = article.find("h3").find("a")
            href = link_tag.get("href")
            # Verifica se o ID está presente no href
            match = re.search(r'_(\d+)/index\.html$', href)
            if match and int(match.group(1)) == id:
                book_url = BOOK_BASE_URL + href
                book_response = requests.get(book_url)
                if book_response.status_code != 200:
                    raise HTTPException(status_code=404, detail="Livro não encontrado")

                book_soup = BeautifulSoup(book_response.text, "html.parser")
                title = book_soup.find("div", class_="product_main").find("h1").text
                price = book_soup.find("p", class_="price_color").text
                availability = book_soup.find("p", class_="instock availability").text.strip()
                description_tag = book_soup.find("div", id="product_description")
                description = description_tag.find_next_sibling("p").text if description_tag else "Sem descrição"
                category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

                return {
                    "id": id,
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "description": description,
                    "category": category,
                    "url": book_url
                }

    raise HTTPException(status_code=404, detail="Livro com ID especificado não encontrado")
# Busca livros por título e/ou categoria.
@router.get("/search", tags=["Endpoints Principais"])
async def Retorna_detalhes_de_um_livro_por_titulo_ou_categoria(
    category: Optional[str] = Query(None, description="Nome da categoria (ex: Science, Travel)"),
    title: Optional[str] = Query(None, description="Parte do título do livro (opcional)"),
    max_pages: int = Query(50, description="Número máximo de páginas a buscar")
):
    base_url = "https://books.toscrape.com"
    livros = []

    async with httpx.AsyncClient() as client:
        # Buscar categorias disponíveis
        response = await client.get(base_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Erro ao acessar o site")

        soup = BeautifulSoup(response.text, 'html.parser')
        categorias = soup.select('ul.nav-list ul li a')

        categoria_url = None
        if category:
            for cat in categorias:
                nome = cat.text.strip()
                if nome.lower() == category.lower():
                    href = cat['href']
                    categoria_url = f"{base_url}/{href}"
                    break
            if not categoria_url:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")
        else:
            categoria_url = f"{base_url}/catalogue/page-1.html"

        # Navegar pelas páginas da categoria ou geral
        for page in range(1, max_pages + 1):
            url = categoria_url.replace("index.html", f"page-{page}.html") if page > 1 else categoria_url
            response = await client.get(url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            livros_html = soup.select('article.product_pod')
            if not livros_html:
                break

            for livro in livros_html:
                titulo = livro.h3.a['title']
                preco = livro.select_one('p.price_color').text.strip()
                link_relativo = livro.h3.a['href']
                link_completo = f"{base_url}/catalogue/{link_relativo}"

                if (title is None or title.lower() in titulo.lower()):
                    livros.append({
                        "titulo": titulo,
                        "preco": preco,
                        "link": link_completo
                    })

    return {
        "categoria": category or "Todas",
        "filtro_titulo": title,
        "quantidade": len(livros),
        "livros": livros
    }

#  Lista todas as categorias de livros disponíveis. 
@router.get("/categories", tags=["Endpoints Principais"])
async def Lista_todas_as_categorias_de_livros_disponiveis():
    categorias = dados_books.find('ul', class_='nav nav-list').find_all('a')
    lista_categorias = [
        categoria.get_text(strip=True)
        for categoria in categorias
          if categoria.get_text(strip=True) != 'Books'
    ]
    return {"categorias": lista_categorias} 




# Endpoints Opcionais da API 

# Estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings)
@router2.get("/overview", tags=["Endpoints Opcionais"])
async def Estatísticas_gerais_da_coleção():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    total_livros = 0
    total_preco = 0.0
    ratings_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            url = base_url.format(page)
            response = await client.get(url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            livros_html = soup.find_all('article', class_='product_pod')
            if not livros_html:
                break                           
            for livro in livros_html:
                total_livros += 1
                preco_text = livro.find('p', class_='price_color').text
                preco = float(re.sub(r'[^0-9.]', '', preco_text))
                total_preco += preco

                rating_class = livro.find('p', class_='star-rating')['class']
                rating = next((i for i in range(1, 6) if f'star-rating {["One", "Two", "Three", "Four", "Five"][i-1]}' in ' '.join(rating_class)), None)
                if rating:
                    ratings_count[rating] += 1                          



            page += 1
    preco_medio = total_preco / total_livros if total_livros > 0 else 0 
    return {
        "total_livros": total_livros,
        "preco_medio": round(preco_medio, 2),
        "distribuicao_ratings": ratings_count
    }
# Estatísticas detalhadas por categoria (quantidade de livros, preços por categoria)
@router2.get("/categories", tags=["Endpoints Opcionais"])
async def Estatísticas_detalhadas_por_categoria():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    categoria_stats = {}
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            url = base_url.format(page)
            response = await client.get(url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            livros_html = soup.find_all('article', class_='product_pod')
            if not livros_html:
                break               
            for livro in livros_html:
                category = livro.find_next('h3').find('a')['title']
                preco_text = livro.find('p', class_='price_color').text
                preco = float(re.sub(r'[^0-9.]', '', preco_text))

                if category not in categoria_stats:
                    categoria_stats[category] = {
                        "quantidade_livros": 0,
                        "preco_total": 0.0
                    }

                categoria_stats[category]["quantidade_livros"] += 1
                categoria_stats[category]["preco_total"] += preco
            page += 1
    for category, stats in categoria_stats.items():
        stats["preco_medio"] = round(stats["preco_total"] / stats["quantidade_livros"], 2) if stats["quantidade_livros"] > 0 else 0.0
        del stats["preco_total"]
    return categoria_stats

# Lista os livros com melhor avaliação (rating mais alto).
@router.get("/top-rated", tags=["Endpoints Opcionais"])
async def Lista_os_livros_com_melhor_avaliação():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    top_rated_books = []
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            url = base_url.format(page)
            response = await client.get(url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            livros_html = soup.find_all('article', class_='product_pod')
            if not livros_html:
                break   
            for livro in livros_html:
                rating_class = livro.find('p', class_='star-rating')['class']
                rating = next((i for i in range(1, 6) if f'star-rating {["One", "Two", "Three", "Four", "Five"][i-1]}' in ' '.join(rating_class)), None)
                if rating == 5:
                    titulo = livro.h3.a['title']
                    preco = livro.select_one('p.price_color').text.strip()
                    link_relativo = livro.h3.a['href']
                    link_completo = f"https://books.toscrape.com/catalogue/{link_relativo}"
                    top_rated_books.append({
                        "titulo": titulo,
                        "preco": preco,
                        "link": link_completo
                    }) 
            page += 1
    return {
        "quantidade_top_rated": len(top_rated_books),
        "top_rated_books": top_rated_books
    }

# Filtra livros dentro de uma faixa de preço específica. 
@router.get('price-range', tags=["Endpoints Opcionais"])
async def Filtra_livros_dentro_de_uma_faixa_de_preço_específica(
    min: float = Query(..., description="Preço mínimo"),          
    max: float = Query(..., description="Preço máximo")
):
    if min < 0 or max < 0 or min > max:
        raise HTTPException(status_code=400, detail="Faixa de preço inválida")
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    livros_filtrados = []
    page = 1
    async with httpx.AsyncClient() as client:
        while True:
            url = base_url.format(page)
            response = await client.get(url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            livros_html = soup.find_all('article', class_='product_pod')
            if not livros_html:
                break
            for livro in livros_html:
                preco_text = livro.find('p', class_='price_color').text
                preco = float(re.sub(r'[^0-9.]', '', preco_text))
                if min <= preco <= max:
                    titulo = livro.h3.a['title']
                    link_relativo = livro.h3.a['href']
                    link_completo = f"https://books.toscrape.com/catalogue/{link_relativo}"
                    livros_filtrados.append({
                        "titulo": titulo,
                        "preco": preco_text,
                        "link": link_completo
                    })
            page += 1
    return {
        "faixa_preco": {"min": min, "max": max},
        "quantidade": len(livros_filtrados),
        "livros": livros_filtrados
    }