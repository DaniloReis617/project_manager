import streamlit as st
from database import execute_query, fetch_all
from auth import get_current_user

def render():
    user = get_current_user()
    if user['role'] not in ['dev','admin', 'manager']:
        st.error("Access denied. Only admins, managers, and devs can add projects.")
        return

    st.subheader("Adicionar Novo Projeto")

    with st.form(key='project_form',border=True):
        company_id = user['company_id']
        project_name = st.text_input("Nome do Projeto")
        start_date = st.date_input("Data de Início")
        end_date = st.date_input("Data de Término")
        status = st.selectbox("Status", ["Não Iniciado", "Cancelado", "Em Andamento", "Concluído"])
        submit_button = st.form_submit_button(label='Adicionar Projeto')

        if submit_button:
            execute_query("INSERT INTO projects (company_id, name, start_date, end_date, status, manager_id) VALUES (?, ?, ?, ?, ?, ?)",
                          (company_id, project_name, start_date, end_date, status, user['id']))
            st.success(f"Projeto '{project_name}' adicionado com sucesso!")
