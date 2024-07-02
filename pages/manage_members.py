import streamlit as st
import pandas as pd
from database import execute_query, fetch_all
from auth import hash_password

def render():
    st.subheader("Manage Members")
    st.write("Add, edit or remove members of the company")

    with st.form(key='add_member_form',border=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        role = st.selectbox("Role", ["user", "manager"])
        company_id = st.number_input("Company ID", min_value=1)
        submit_button = st.form_submit_button(label='Add Member')

        if submit_button:
            try:
                hashed_password = hash_password(password)
                execute_query("INSERT INTO users (username, password, role, company_id) VALUES (?, ?, ?, ?)",
                              (username, hashed_password, role, company_id))
                st.success("Member added successfully")
            except Exception as e:
                st.error(f"Error adding member: {e}")

    st.subheader("Current Members")
    members = fetch_all("SELECT id, username, role FROM users")
    df = pd.DataFrame(members, columns=['ID', 'Username', 'Role'])
    st.dataframe(df ,use_container_width=True)

    member_id = st.number_input("Member ID to Edit/Delete", min_value=1)

    with st.form(key='edit_member_form',border=True):
        new_username = st.text_input("New Username")
        new_role = st.selectbox("New Role", ["user", "manager", "admin"])
        update_button = st.form_submit_button(label='Update Member')

        if update_button:
            try:
                execute_query("UPDATE users SET username = ?, role = ? WHERE id = ?",
                              (new_username, new_role, member_id))
                st.success("Member updated successfully")
            except Exception as e:
                st.error(f"Error updating member: {e}")

    delete_button = st.button("Delete Member")

    if delete_button:
        try:
            execute_query("DELETE FROM users WHERE id = ?", (member_id,))
            st.success("Member deleted successfully")
        except Exception as e:
            st.error(f"Error deleting member: {e}")
