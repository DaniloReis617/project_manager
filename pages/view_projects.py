import streamlit as st
import pandas as pd
from database import fetch_all
from auth import get_current_user

def render():
    user = get_current_user()
    st.subheader("Visualizar Projetos")

    if user['role'] == 'dev':
        data = fetch_all("SELECT * FROM projects")
    elif user['role'] == 'admin':
        data = fetch_all("SELECT * FROM projects WHERE company_id = ?", (user['company_id'],))
    else:  # manager or user
        data = fetch_all("""
            SELECT p.* FROM projects p
            JOIN team_members t ON p.id = t.project_id
            WHERE t.user_id = ?
        """, (user['id'],))
    
    df = pd.DataFrame(data, columns=['ID', 'Company ID', 'Nome do Projeto', 'Data de Início', 'Data de Término', 'Status', 'Manager ID'])
    st.dataframe(df, use_container_width=True)


