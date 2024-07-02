import streamlit as st
from database import execute_query, fetch_all
from auth import get_current_user

def render():
    user = get_current_user()

    st.subheader("Adicionar Nova Tarefa")

    projects = fetch_all("SELECT id, name FROM projects WHERE company_id = ?", (user['company_id'],))
    project_options = {name: id for id, name in projects}

    if not project_options:
        st.warning("Nenhum projeto encontrado. Adicione um projeto primeiro.")
        return

    project_name = st.selectbox("Selecionar Projeto", list(project_options.keys()))
    project_id = project_options[project_name]

    with st.form(key='task_form',border=True):
        task_name = st.text_input("Nome da Tarefa")
        task_status = st.selectbox("Status", ["Pendente", "Em Progresso", "Concluído"])
        task_progress = st.slider("Progresso", 0, 100)
        submit_button = st.form_submit_button(label='Adicionar Tarefa')

        if submit_button:
            execute_query("INSERT INTO tasks (project_id, name, status, progress) VALUES (?, ?, ?, ?)",
                          (project_id, task_name, task_status, task_progress))
            st.success(f"Tarefa '{task_name}' adicionada com sucesso!")
