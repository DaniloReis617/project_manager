import streamlit as st
import pandas as pd
from auth import get_current_user
from database import get_projects_by_manager, get_users_by_company, add_user_to_team, get_team_members

def render():
    user = get_current_user()

    if user['role'] in ['dev', 'manager']:
        st.error("Access denied. Only managers can manage teams.")
        return

    st.subheader("Manage Team")
    st.write("Add users to the project team")

    projects = get_projects_by_manager(user['id'])
    project_options = {name: id for id, name in projects}

    if not project_options:
        st.warning("You are not managing any projects.")
        return

    project_name = st.selectbox("Select Project", list(project_options.keys()))
    project_id = project_options[project_name]

    users = get_users_by_company(user['company_id'])
    user_options = {username: id for id, username in users}

    if not user_options:
        st.warning("No users available to add.")
        return

    username = st.selectbox("Select User", list(user_options.keys()))
    user_id = user_options[username]

    add_button = st.button("Add to Team")

    if add_button:
        try:
            add_user_to_team(project_id, user_id)
            st.success("User added to the team successfully")
        except Exception as e:
            st.error(f"Error adding user to the team: {e}")

    st.subheader("Current Team Members")
    team_members = get_team_members(user['id'])
    df = pd.DataFrame(team_members, columns=['Username', 'Project'])
    st.dataframe(df, use_container_width=True)
