import streamlit as st
import hashlib
from database import fetch_all, execute_query

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, role='user', company_id=None):
    hashed_password = hash_password(password)
    execute_query("INSERT INTO users (username, email, password, role, company_id) VALUES (?, ?, ?, ?, ?)",
                  (username, email, hashed_password, role, company_id))

def login_user(email, password):
    hashed_password = hash_password(password)
    user = fetch_all("SELECT * FROM users WHERE email = ?", (email,))
    if not user:
        return "user_not_found"
    stored_password = user[0][3]
    if hashed_password != stored_password:
        return "incorrect_password"
    user_data = {
        'id': user[0][0],
        'username': user[0][1],
        'email': user[0][2],
        'role': user[0][4],
        'company_id': user[0][5]
    }
    return user_data  # Retorna um dicionário com os dados do usuário

def check_existing_email(email):
    user = fetch_all("SELECT id FROM users WHERE email = ?", (email,))
    return bool(user)

def register_user(username, email, password, role, company_id=None):
    create_user(username, email, password, role, company_id=company_id)

def get_current_user():
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state.user

def set_current_user(user):
    st.session_state.user = user

def update_user_password(user_id, new_password):
    hashed_password = hash_password(new_password)
    execute_query("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
