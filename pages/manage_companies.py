import streamlit as st
import pandas as pd
from database import execute_query, fetch_all
from auth import get_current_user

def render():
    user = get_current_user()
    if user['role'] not in ['dev', 'admin']:
        st.error("Access denied. Only admins and devs can manage companies.")
        return

    st.subheader("Gerenciar Empresas")

    # Formulário para adicionar nova empresa
    with st.form(key='company_form'):
        company_name = st.text_input("Nome da Empresa")
        submit_button = st.form_submit_button(label='Adicionar Empresa')

        if submit_button and company_name:
            execute_query("INSERT INTO companies (name) VALUES (?)", (company_name,))
            st.success(f"Empresa '{company_name}' adicionada com sucesso!")
            st.experimental_rerun()

    # Seleção de empresa para visualizar e editar
    st.subheader("Selecionar Empresa para Visualizar/Editar Usuários")
    companies = fetch_all("SELECT id, name FROM companies")
    company_dict = {name: id for id, name in companies}
    company_name = st.selectbox("Selecionar Empresa", list(company_dict.keys()))

    if company_name:
        company_id = company_dict[company_name]
        st.subheader(f"Usuários da Empresa: {company_name}")

        if user['role'] == 'dev':
            users = fetch_all("SELECT id, username, email, role FROM users WHERE company_id = ?", (company_id,))
            df = pd.DataFrame(users, columns=['ID', 'Username', 'Email', 'Role'])
            st.dataframe(df)

            st.subheader("Editar Usuário")
            selected_user = st.selectbox("Selecionar Usuário", df['ID'])
            new_username = st.text_input("Novo Nome de Usuário")
            new_email = st.text_input("Novo Email")
            new_role = st.selectbox("Novo Perfil", ["user", "manager", "admin", "dev"])
            submit_edit_button = st.button("Salvar Alterações")

            if submit_edit_button:
                execute_query("UPDATE users SET username = ?, email = ?, role = ?, company_id = ? WHERE id = ?",
                              (new_username, new_email, new_role, company_id, selected_user))
                st.success("Usuário atualizado com sucesso!")
                st.experimental_rerun()

        elif user['role'] == 'admin' and user['company_id'] == company_id:
            users = fetch_all("SELECT id, username, email, role FROM users WHERE company_id = ?", (company_id,))
            df = pd.DataFrame(users, columns=['ID', 'Username', 'Email', 'Role'])
            st.dataframe(df)

            st.subheader("Adicionar Usuário à Empresa")
            new_username = st.text_input("Nome de Usuário")
            new_email = st.text_input("Email")
            new_role = st.selectbox("Perfil", ["user", "manager", "admin"])
            new_password = st.text_input("Senha", type='password')
            submit_add_user_button = st.button("Adicionar Usuário")

            if submit_add_user_button:
                execute_query("INSERT INTO users (username, email, password, role, company_id) VALUES (?, ?, ?, ?, ?)",
                              (new_username, new_email, new_password, new_role, company_id))
                st.success("Usuário adicionado com sucesso!")
                st.experimental_rerun()
