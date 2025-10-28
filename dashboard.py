# Importação necessárias
import streamlit as st
import requests
import pandas as pd

API_URL = "https://techchallengewesleyrodrigues-5.onrender.com/api/v1/books/"

st.title("📚 Dashboard - api/v1/books/")

# Campo para inserir o token JWT
token = st.text_input("Insira seu token JWT", type="password")

if token:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        livros = response.json().get("livros", [])
        df = pd.DataFrame(livros, columns=["Título"])
        st.subheader("Lista de Livros")
        st.dataframe(df)
        st.success(f"{len(df)} livros encontrados.")
    else:
        st.error(f"Erro ao buscar livros: {response.status_code}")
else:
    st.info("Insira seu token JWT para visualizar os livros.")


