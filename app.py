import streamlit as st
import re
from auth import login_user, register_user, check_existing_email, get_current_user, set_current_user
from pages import home, profile, manage_members, add_project, add_task, view_projects, view_tasks, manage_team, manage_companies

# Configuração da página do Streamlit
st.set_page_config(page_title="Project Manager", page_icon="📊", layout="wide")

def main():
    user = get_current_user()

    if user:
        if st.sidebar.button("Recarregar Aplicativo"):
            st.experimental_rerun()

        menu = ["Home", "Profile", "View Projects", "View Tasks", "Logout"]
        if user['role'] in ['admin', 'manager', 'dev']:
            menu.insert(1, "Add Project")
        if user['role'] in ['admin', 'dev']:
            menu.insert(2, "Manage Companies")
        if user['role'] == 'admin':
            menu.insert(3, "Manage Members")
        if user['role'] in ['manager', 'dev']:
            menu.insert(4, "Manage Team")
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            home.render()
        elif choice == "Profile":
            profile.render()
        elif choice == "Add Project":
            add_project.render()
        elif choice == "Manage Companies":
            manage_companies.render()
        elif choice == "Manage Members":
            manage_members.render()
        elif choice == "Manage Team":
            manage_team.render()
        elif choice == "View Projects":
            view_projects.render()
        elif choice == "View Tasks":
            view_tasks.render()
        elif choice == "Logout":
            st.session_state.user = None
            st.experimental_rerun()
    else:
        st.title("Project Manager")
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            with st.container():
                with st.form(key='login_form'):
                    st.subheader("Login")
                    email = st.text_input("Email", placeholder="Digite seu Email")
                    # Verifica se o email é válido
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        st.error("Por favor, insira um email válido.")
                    password = st.text_input("Senha", placeholder="Digite sua senha", type='password')
                    if st.form_submit_button('Entrar'):
                        result = login_user(email, password)
                        if result == "user_not_found":
                            st.error('Usuário não encontrado.')
                        elif result == "incorrect_password":
                            st.error('Senha incorreta.')
                        elif result:
                            st.session_state.user = result
                            st.session_state.logged_in = True
                            st.success(f'Login realizado com sucesso como {email}!')
                            st.experimental_rerun()  # Redireciona para a tela Home
                        else:
                            st.error('Erro desconhecido. Por favor, tente novamente.')

        elif choice == "Register":
            with st.container():
                col1, col2, col3 = st.columns([0.5, 8, 0.5])
                with col2:
                    st.subheader("Registro")
                    with st.form(key='register_form'):
                        # Campo para inserir novo email
                        new_email = st.text_input("E-mail", placeholder="Digite seu Email")
                        # Verifica se o email é válido
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                            st.error("Por favor, insira um email válido.")
                        # Campo para inserir novo nome de usuário
                        new_username = st.text_input("Nome de Usuário", placeholder="Digite seu nome de usuário")
                        # Campo para selecionar o perfil do usuário
                        new_role = st.selectbox("Perfil", ["user", "manager", "admin", "dev"])
                        # Campo para inserir nova senha
                        new_password = st.text_input("Nova Senha", placeholder="Digite sua senha", type='password')
                        # Campo para confirmar a nova senha
                        confirm_password = st.text_input("Confirme a Nova Senha", placeholder="Digite sua senha novamente", type='password')
                        # Verifica se a senha e a confirmação coincidem
                        if new_password != confirm_password:
                            st.error("As senhas digitadas não coincidem. Por favor, tente novamente.")
                        # Botão para submeter o formulário de registro
                        if st.form_submit_button('Criar Conta'):
                            # Verifica se o email já está em uso
                            existing_user = check_existing_email(new_email)
                            if existing_user:
                                st.error(f'O email "{new_email}" já está em uso. Por favor, escolha outro.')
                            else:
                                # Registra o usuário se o email não estiver em uso
                                register_user(new_username, new_email, new_password, new_role)
                                st.success(f'Conta registrada com sucesso para {new_email}!')
                                return True  # Retorna True se o registro for bem-sucedido

if __name__ == "__main__":
    main()
