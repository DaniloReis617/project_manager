import sqlite3
from contextlib import closing

def get_connection():
    return sqlite3.connect('project_manager.db')

def execute_query(query, params=()):
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, params)
            conn.commit()

def fetch_all(query, params=()):
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

def get_projects_by_manager(manager_id):
    return fetch_all("SELECT id, name FROM projects WHERE manager_id = ?", (manager_id,))

def get_users_by_company(company_id):
    return fetch_all("SELECT id, username FROM users WHERE company_id = ?", (company_id,))

def add_user_to_team(project_id, user_id):
    execute_query("INSERT INTO team_members (project_id, user_id) VALUES (?, ?)", (project_id, user_id))

def get_team_members(manager_id):
    return fetch_all("""
        SELECT users.username, projects.name 
        FROM team_members 
        JOIN users ON team_members.user_id = users.id 
        JOIN projects ON team_members.project_id = projects.id
        WHERE projects.manager_id = ?
    """, (manager_id,))
