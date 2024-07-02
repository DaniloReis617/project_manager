from database import fetch_all

def get_project_names():
    projects = fetch_all("SELECT name FROM projects")
    return [project[0] for project in projects]
