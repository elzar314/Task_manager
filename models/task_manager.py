from data.data_manager import DataManager

class TaskManager:
    """Clase para gestionar las operaciones con tareas"""
    
    # Definición de prioridades para ordenamiento de tareas
    PRIORITY_ORDER = {"Alta": 1, "Media": 2, "Baja": 3}
    DATA_FILE = "tasks.json"
    
    def __init__(self):
        self.tasks = DataManager.load_data(self.DATA_FILE, [])
    
    def add_task(self, task_data):
        """Añade una nueva tarea"""
        self.tasks.append(task_data)
        self.save_tasks()
    
    def delete_task(self, task):
        """Elimina una tarea existente"""
        self.tasks.remove(task)
        self.save_tasks()
    
    def toggle_complete(self, task):
        """Marca o desmarca una tarea como completada"""
        task["completed"] = not task.get("completed", False)
        self.save_tasks()
    
    def save_tasks(self):
        """Guarda todas las tareas en el archivo"""
        DataManager.save_data(self.tasks, self.DATA_FILE)
    
    def get_filtered_tasks(self, project_name=None):
        """Obtiene tareas filtradas por proyecto"""
        if project_name:
            return [t for t in self.tasks if t.get("project", "Sin Proyecto") == project_name]
        return self.tasks
    
    def get_sorted_tasks(self, tasks_to_sort=None):
        """Ordena las tareas por prioridad"""
        tasks_to_sort = tasks_to_sort or self.tasks
        return sorted(tasks_to_sort, key=lambda x: self.PRIORITY_ORDER.get(x.get("priority", "Media"), 2))