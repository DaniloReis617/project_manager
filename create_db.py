import hashlib
from database import execute_query

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Criação de tabela de empresas
execute_query('''
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Criação de tabela de usuários
execute_query('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'user', 'dev')),
    company_id INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies (id)
)
''')

# Criação de tabela de projetos
execute_query('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies (id),
    FOREIGN KEY (manager_id) REFERENCES users (id)
)
''')

# Criação de tabela de tarefas
execute_query('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    progress INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (id)
)
''')

# Criação de tabela de equipes
execute_query('''
CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Inserir usuário DEV com os detalhes fornecidos
hashed_password = hash_password('danilo21')
execute_query('''
INSERT INTO users (username, email, password, role, company_id)
VALUES (?, ?, ?, ?, NULL)
''', ('danilo', 'daniloreis2196@gmail.com', hashed_password, 'dev'))
