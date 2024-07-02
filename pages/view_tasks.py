import streamlit as st
import pandas as pd
from database import fetch_all
from auth import get_current_user

def render():
    user = get_current_user()

    st.subheader("Visualizar Tarefas")

    data = fetch_all("SELECT tasks.id, projects.name, tasks.name, tasks.status, tasks.progress FROM tasks JOIN projects ON tasks.project_id = projects.id WHERE projects.company_id = ?", (user['company_id'],))
    df = pd.DataFrame(data, columns=['ID', 'Projeto', 'Tarefa', 'Status', 'Progresso'])
    st.dataframe(df,use_container_width=True)
