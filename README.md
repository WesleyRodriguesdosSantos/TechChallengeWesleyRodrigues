Wesley Rodrigues dos santos-RM368423


## 🌐 Link do meu Repositório GitHub
https://github.com/WesleyRodriguesdosSantos/TechChallengeWesleyRodrigues/tree/main

## 🌐 Link do Deploy
https://techchallengewesleyrodrigues-5.onrender.com/docs

## 🎥 Link do Vídeo
https://drive.google.com/file/d/1_RCCTnpAQi_0Ho3D0hUpfsWmQFO5fmnv/view?usp=sharing

## 🎓  Link do curso no Google Cloud Skill Boost
https://www.skills.google/public_profiles/0a833a9b-da3a-4ac8-b1fa-14fc259427a5/badges/19513138

## 🧭 Diagrama de Arquitetura
[Plano Arquitetural - Wesley Rodrigues dos santos-RM368423.docx](https://github.com/user-attachments/files/23224465/Plano.Arquitetural.-.Wesley.Rodrigues.dos.santos-RM368423.docx)

## 📊 Planilha com logs de todas as chamadas e a base ususarios.db
[Wesley Rodrigues dos santos-RM368423 - Logs - usuarios.db.xlsx](https://github.com/user-attachments/files/23224949/Wesley.Rodrigues.dos.santos-RM368423.-.Logs.-.usuarios.db.xlsx)


# 📚 Tech Challenge - API de Scraping de Livros

# 📘 Descrição do Projeto

Este projeto se trata de uma API desenvolvida com FastAPI que tem por objetivo realizazr um Web Scraping no site: https://books.toscrape.com , para que possa ser realizados consultas como : listar todos os livros disponíveis, retorna detalhes completos de um livro específico, busca livros por título e/ou categoria, listar todas as categorias de livros disponíveis e verifica status da API e conectividade com os dados.
Essa aplicação foi desenvolvida como parte de um desafio técnico de pós-graduação em Machine Learning Engineering, para colocarmos em prática os conhecimentos aprendidos referente a integração de dados externos, Web Scraping, boas práticas de arquitetura de software.




## 🏗️ Arquitetura do Projeto
A arquitetura segue uma estrutura modular e escalável, com os seguintes componentes principais:
🔹 FastAPI
Framework principal para construção da API, escolhido por sua performance, suporte a tipagem e documentação automática via Swagger.
🔹 httpx + asyncio
Cliente HTTP assíncrono que permite realizar múltiplas requisições simultâneas às páginas de livros, acelerando o processo de scraping.
🔹 BeautifulSoup
Biblioteca de parsing HTML utilizada para extrair os dados estruturados das páginas web.
🔹 Uvicorn
Servidor ASGI utilizado para executar a aplicação localmente com suporte a hot reload durante o desenvolvimento.



## 📁 Estrutura de Diretórios
├── main.py                  # Ponto de entrada da aplicação

├── core

│   └── __init__.py          # Importação necessária

│   └── auth.py              # Modulo de autenticação

│   └── crud.py              # Modulo com esquema bcrypt para garantir a segurança das senhas dos usuários

│   └── database.py          # SQLAlchemy com SQLite para persistência de dados

│   └── models.py            # Modelo de usuario(SQLAlchemy)

│   └── schemas.py           # Pydantic Models

├── routes

│   └── books.py             # Rotas principais da API

│   └── health.py            # Modulo para verifica a saúde da API e conectividade com os dados

│   └──__init__.py           # Importação necessária

├── requirements.txt         # Dependencias necessárias para o projeto

├── dashboard.py             # Interface visual

├── README.md                # Documentação do projeto

├── usuarios.db              # Armazena os usuarios cadastrados



# 🛠️ Instalação e Configuração

## 1. Clone o repositório: 
Bash:
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

## 2. Crie e ative o ambiente virtual
Bash:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

## 3. Instale as dependências
Bash:
pip install -r requirements.txt


# ▶️ Instruções para Execução

## 1. Execute o servidor local
Bash:
uvicorn main:app --reload

## 2. Acesse a interface Swagger gerada pelo FastAPI
Abra no navegador:
http://127.0.0.1:8000/docs

## 3. Acesse para leitura e navegação detalhada
Abra no navegador:
http://127.0.0.1:8000/redoc



## 4. Instruções para Execução do Dashboard - (Streamlit)

Abra um segundo terminal:
Bash:
streamlit run dashboard.py




# 🔐 Instruções para Autenticação JWT na API: auth.py
Esta API ultiliza autenticação HTTP Basic para proteger seus endpoints.

## 📚 Endpoint: Criar usuário

1. Vá até o endpoint POST /usuarios/
Clique em "Try it out"
Preencha o corpo da requisição com:
JSON{  "username": "seu_nome",  "senha": "senha123"}
Clique em "Execute"
Você verá a resposta com os dados do usuário criado.

2. Fazer login e obter o token JWT

Vá até o endpoint POST /token
Clique em "Try it out"
Preencha os campos:

username: seu_nome
password: senha123

Clique em "Execute"
A resposta será algo como:

JSON{  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  "token_type": "bearer"}
Copie o valor de access_token.

3. Autenticar no Swagger para acessar rotas protegidas
No topo da página do Swagger, clique em "Authorize"
No campo que aparece, digite:

username: seu_nome
password: senha123
client_id: Bearer
client_secret: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(access_token)

Clique em "Authorize" e depois em "Close"

4. Acessar rota protegida /auth
Vá até o endpoint GET /me
Clique em "Try it out"
Clique em "Execute"
Se o token for válido, você verá os dados do usuário autenticado.



# 📚 Endpoint: Listar Todos os Livros Disponíveis
Este Endpoint contém uma rota para listar todos os títulos de livros disponíveis.

## 'GET/api/v1/books'

## Parâmetros de Consulta
Não é necessário parametros.

### Exemplo de requisição
'GET'\'http://127.0.0.1:8000/api/v1/books/'

### Exemplo de Resposta
```json
{
  "livros": [
    "A Light in the Attic",
    "Tipping the Velvet",
    "Soumission",
    "Sharp Objects",
    "Sapiens: A Brief History of Humankind",
    "The Requiem Red",
    "The Dirty Little Secrets of Getting Your Dream Job",
    "..."
  ]
}
```


# 📚 Endpoint:  Retorna detalhes completos de um livro específico pelo ID

Este endpoint realiza a busca detalhada de um livro específico no site Books to Scrape, utilizando o ID fornecido como parâmetro e extrai os seguintes dados:Título , Preço, Disponibilidade, Descrição, Categoria e URL completa do livro.

## 'GET/api/v1/books/998

## Parâmetros de Consulta
 - ID -  ID presente no padrão _<id>/index.html da URL da página.

### Exemplo de Requisição
'GET'\'http://127.0.0.1:8000/api/v1/books/998'

### Exemplo de Resposta
```json
{
  "id": 998,
  "title": "Soumission",
  "price": "Â£50.10",
  "availability": "In stock (20 available)",
  "description": "Dans une France assez proche de la nÃ´tre, un homme sâengage dans la carriÃ¨re universitaire. Peu motivÃ© par lâenseignement, il sâattend Ã  une vie ennuyeuse mais calme, protÃ©gÃ©e des grands drames historiques. Cependant les forces en jeu dans le pays ont fissurÃ© le systÃ¨me politique jusquâÃ  provoquer son effondrement. Cette implosion sans soubresauts, sans vraie rÃ©volution, s Dans une France assez proche de la nÃ´tre, un homme sâengage dans la carriÃ¨re universitaire. Peu motivÃ© par lâenseignement, il sâattend Ã  une vie ennuyeuse mais calme, protÃ©gÃ©e des grands drames historiques. Cependant les forces en jeu dans le pays ont fissurÃ© le systÃ¨me politique jusquâÃ  provoquer son effondrement. Cette implosion sans soubresauts, sans vraie rÃ©volution, se dÃ©veloppe comme un mauvais rÃªve.Le talent de lâauteur, sa force visionnaire nous entraÃ®nent sur un terrain ambigu et glissant ; son regard sur notre civilisation vieillissante fait coexister dans ce roman les intuitions poÃ©tiques, les effets comiques, une mÃ©lancolie fataliste.Ce livre est une saisissante fable politique et morale. ...more",
  "category": "Fiction",
  "url": "https://books.toscrape.com/catalogue/soumission_998/index.html"
}
```


# 📚 Endpoint: Detalhes de Livros por Título e/ou Categoria
Este Endpoint lista de livros com base em filtros opcionais de título e categoria, com detalhes como título, preço e link.

## 'GET/api/v1/books/search'

## Parâmetros de Consulta
- category - (obrigatório): Nome da categoria de livros (ex: "Travel","Mystery","Historical Fiction")
- title - (opcional): Parte do título do livro para filtrar os resultados
- max_pages - (opcional): Número máximo de páginas a buscar (padrão: 50)

### Exemplo de Requisição
'GET'\'http://127.0.0.1:8000/api/v1/books/search?title=In%20a%20Dark%2C%20Dark%20Wood&max_pages=50'

### Exemplo de Resposta
```json
{
  "categoria": "Science",
  "filtro_titulo": "physics",
  "quantidade": 1,
  "livros": [
    {
      "titulo": "Seven Brief Lessons on Physics",
      "preco": "£30.60",
      "link": "https://books.toscrape.com/catalogue/../../../seven-brief-lessons-on-physics_219/index.html"
    }
  ]
}
```



# 📚 Endpoint: Listar Categorias de Livros
Este endpoint retornar uma lista com os nomes das categorias de livros disponíveis no site.

## 'GET/api/v1/books/categories'

## Parâmetros de Consulta
Não é necessário parametros.

### Exemplo de Requisição
'GET'\http://127.0.0.1:8000/api/v1/books/categories

### Exemplo de Resposta
```json
{
  "categorias": [
    "Travel",
    "Mystery",
    "Historical Fiction",
    "Science Fiction",
    "Classics",
    "Philosophy",
    "Romance",
    "..."
  ]
}
```


# ▶️ Instruções para uso do modulo: health.py 

## GET /health 
Descrição: Verifica a saúde da API e conectividade.

### Request URL
GET /health 
Request URL: http://127.0.0.1:8000/api/v1/health

### Response body
{
  "status": "ok",
  "mensagem": "API está funcionando e conectada ao site Books to Scrape.",
  "site_status": 200
}



# 📚 Endpoint:  Lista os livros com Melhor Avaliação

## 'GET/api/v1/books/top-rated'
Descrição: Este endpoint listar todos os livros com avaliação máxima (5 estrelas)

## Parâmetros de Consulta
Não é necessário parametros.

### Exemplo de Requisição
'GET'\http://127.0.0.1:8000/api/v1/books/top-rated

### Exemplo de Resposta
```json
{
  "quantidade_top_rated": 196,
  "top_rated_books": [
    {
      "titulo": "Sapiens: A Brief History of Humankind",
      "preco": "£54.23",
      "link": "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
    },
    {
      "titulo": "Set Me Free",
      "preco": "£17.46",
      "link": "https://books.toscrape.com/catalogue/set-me-free_988/index.html"
    }
  ]
}
```

# 📚 Endpoint: Filtra livros dentro de uma faixa de preço especifica

## 'GET/api/v1/booksprice-range'
Descrição: Este endpoint listar livros cujo preço esteja dentro de uma faixa definida pelo usuário.

## Parâmetros de Consulta
Preço minimo: valor_digitado(0)
Preço Máximo: valor_digitado(150)

### Exemplo de Requisição
'GET'\http://127.0.0.1:8000/api/v1/booksprice-range?min=0&max=150

### Exemplo de Resposta
```json
{
  "faixa_preco": {
    "min": 0,
    "max": 150
  },
  "quantidade": 1000,
  "livros": [
    {
      "titulo": "A Light in the Attic",
      "preco": "£51.77",
      "link": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    }
 ]
}
```

# 📚 Endpoint: Estatistica gerais da coleção

## 'GET/api/v1/starts/overview
Descrição: Este endpoint gera estatísticas agregadas sobre a coleção de livros disponível. Ele percorre todas as páginas e calcula:
Total de livros
Preço médio
Distribuição de avaliações (ratings de 1 a 5 estrelas)

## Parâmetros de Consulta
Não é necessário parametros.

### Exemplo de Requisição
'GET'\http://127.0.0.1:8000/api/v1/starts/overview

### Exemplo de Resposta
```json
{
  "total_livros": 1000,
  "preco_medio": 35.07,
  "distribuicao_ratings": {
    "1": 226,
    "2": 196,
    "3": 203,
    "4": 179,
    "5": 196
  }
}
```

# 📚 Endpoint: Estatisticas detalhadas por categoria

## 'GET/api/v1/starts/categories
Descrição: Este endpoint gera estatísticas por categoria de livros. Ele percorre todas as páginas disponíveis e agrupa os livros por categoria, calculando:
Quantidade de livros por categoria
Preço médio dos livros em cada categoria

## Parâmetros de Consulta
Não é necessário parametros.

### Exemplo de Requisição
'GET'\http://127.0.0.1:8000/api/v1/starts/categories'

### Exemplo de Resposta
```json
{
  "A Light in the Attic": {
    "quantidade_livros": 1,
    "preco_medio": 51.77
  },
  "Tipping the Velvet": {
    "quantidade_livros": 1,
    "preco_medio": 53.74
  }
}
```


















