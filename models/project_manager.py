import flet as ft
from data.data_manager import DataManager

class ProjectManager:
    """Clase para gestionar las operaciones con proyectos"""
    
    PROJECTS_FILE = "projects.json"
    
    def __init__(self):
        self.projects = DataManager.load_data(self.PROJECTS_FILE, [{"name": "Sin Proyecto", "id": "default"}])
    
    def add_project(self, name):
        """Añade un nuevo proyecto"""
        if name.strip() and not any(p['name'] == name for p in self.projects):
            new_project = {
                "name": name,
                "id": name.lower().replace(" ", "_")
            }
            self.projects.append(new_project)
            self.save_projects()
            return True
        return False
    
    def delete_project(self, project):
        """Elimina un proyecto existente"""
        if project["id"] != "default":
            self.projects.remove(project)
            self.save_projects()
            return True
        return False
    
    def save_projects(self):
        """Guarda todos los proyectos en el archivo"""
        DataManager.save_data(self.projects, self.PROJECTS_FILE)
    
    def get_project_options(self):
        """Obtiene las opciones de proyectos para un dropdown"""
        return [ft.dropdown.Option(p["name"]) for p in self.projects]
    
    def get_sorted_projects(self):
        """Obtiene los proyectos ordenados por nombre"""
        named_projects = [p for p in self.projects if p['name'] != "Sin Proyecto"]
        unnamed_project = [p for p in self.projects if p['name'] == "Sin Proyecto"]
        
        named_projects.sort(key=lambda x: x['name'])
        return named_projects, unnamed_project