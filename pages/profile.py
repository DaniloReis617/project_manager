import streamlit as st
import pandas as pd
from auth import get_current_user, update_user_password, check_existing_email
from database import fetch_all, execute_query

def render():
    user = get_current_user()
    st.subheader("Edit Profile Information")
    
    if user:
        st.subheader("Profile")
        st.write("Username:", user['username'])
        st.write("Email:", user['email'])
        st.write("Role:", user['role'])

        with st.form(key='edit_profile_form'):
            new_username = st.text_input("New Username", value=user['username'])
            new_email = st.text_input("New Email", value=user['email'])
            new_password = st.text_input("New Password", type='password')
            
            if user['role'] == 'dev':
                companies = fetch_all("SELECT id, name FROM companies")
                company_dict = {name: id for id, name in companies}
                new_company = st.selectbox("Company", list(company_dict.keys()), index=list(company_dict.values()).index(user['company_id']) if user['company_id'] else 0)
                new_company_id = company_dict[new_company]

            submit_button = st.form_submit_button(label='Update Profile')

            if submit_button:
                if new_username and new_email:
                    if new_email != user['email'] and check_existing_email(new_email):
                        st.error(f'O email "{new_email}" já está em uso. Por favor, escolha outro.')
                    else:
                        execute_query("UPDATE users SET username = ?, email = ?, company_id = ? WHERE id = ?", (new_username, new_email, new_company_id, user['id']))
                        if new_password:
                            update_user_password(user['id'], new_password)
                        st.success("Profile updated successfully")
                        st.experimental_rerun()
                else:
                    st.error("Username and Email cannot be empty")
    
    if user['role'] == 'dev':
        st.subheader("All Users")
        data = fetch_all("SELECT username, email, role, company_id FROM users")
        df = pd.DataFrame(data, columns=['Username', 'Email', 'Role', 'Company ID'])
        st.dataframe(df, use_container_width=True)
    elif user['role'] == 'admin':
        st.subheader("Users in My Company")
        data = fetch_all("SELECT username, email, role FROM users WHERE company_id = ?", (user['company_id'],))
        df = pd.DataFrame(data, columns=['Username', 'Email', 'Role'])
        st.dataframe(df, use_container_width=True)
    elif user['role'] == 'manager':
        st.subheader("Users in My Team")
        data = fetch_all("""
            SELECT u.username, u.email, u.role FROM users u
            JOIN team_members t ON u.id = t.user_id
            JOIN projects p ON t.project_id = p.id
            WHERE p.manager_id = ?
        """, (user['id'],))
        df = pd.DataFrame(data, columns=['Username', 'Email', 'Role'])
        st.dataframe(df, use_container_width=True)
