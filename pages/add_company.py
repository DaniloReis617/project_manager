import streamlit as st
from database import execute_query
from auth import get_current_user

def render():
    user = get_current_user()
    if user['role'] not in ['dev', 'admin']:
        st.error("Access denied. Only admins and devs can add companies.")
        return

    st.subheader("Adicionar Nova Empresa")

    with st.form(key='company_form'):
        company_name = st.text_input("Nome da Empresa")
        submit_button = st.form_submit_button(label='Adicionar Empresa')

        if submit_button:
            execute_query("INSERT INTO companies (name) VALUES (?)", (company_name,))
            st.success(f"Empresa '{company_name}' adicionada com sucesso!")
            st.experimental_rerun()  # Recarrega a página
