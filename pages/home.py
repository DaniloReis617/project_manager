import streamlit as st
import pandas as pd
from database import fetch_all

def render():
    st.subheader("Visão Kanban dos Projetos")

    # Definindo os status
    status_list = ["Não Iniciado", "Cancelado", "Em Andamento", "Concluído"]

    # Buscando projetos do banco de dados
    projects = fetch_all("SELECT id, name, status FROM projects")
    df = pd.DataFrame(projects, columns=['ID', 'Nome do Projeto', 'Status'])

    # Contando o número de projetos por status
    counts = df['Status'].value_counts().to_dict()

    # Criando colunas para cada status
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 2.5])
    
    with col1:
        st.header(f"Não Iniciado ({counts.get('Não Iniciado', 0)})")
        status_projects = df[df['Status'] == "Não Iniciado"]
        for _, row in status_projects.iterrows():
            with st.container(border=True):
                st.write(f"ID: {row['ID']}")
                st.write(f"Nome do Projeto: {row['Nome do Projeto']}")
                st.write("---")

    with col2:
        st.header(f"Cancelado ({counts.get('Cancelado', 0)})")
        status_projects = df[df['Status'] == "Cancelado"]
        for _, row in status_projects.iterrows():
            with st.container(border=True):
                st.write(f"ID: {row['ID']}")
                st.write(f"Nome do Projeto: {row['Nome do Projeto']}")
                st.write("---")

    with col3:
        st.header(f"Em Andamento ({counts.get('Em Andamento', 0)})")
        status_projects = df[df['Status'] == "Em Andamento"]
        for _, row in status_projects.iterrows():
            with st.container(border=True):
                st.write(f"ID: {row['ID']}")
                st.write(f"Nome do Projeto: {row['Nome do Projeto']}")
                st.write("---")

    with col4:
        st.header(f"Concluído ({counts.get('Concluído', 0)})")
        status_projects = df[df['Status'] == "Concluído"]
        for _, row in status_projects.iterrows():
            with st.container(border=True):
                st.write(f"ID: {row['ID']}")
                st.write(f"Nome do Projeto: {row['Nome do Projeto']}")
                st.write("---")
