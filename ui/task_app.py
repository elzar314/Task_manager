import flet as ft
from datetime import datetime
from models.task_manager import TaskManager
from models.project_manager import ProjectManager

class TaskApp:
    """Clase principal de la aplicación"""
    
class TaskApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.task_manager = TaskManager()
        self.project_manager = ProjectManager()
        
        # Configuración inicial de la página
        self.page.title = "Proyecto Final - Gestor de Tareas"
        self.page.theme_mode = ft.ThemeMode.DARK
        
        # Inicialización de componentes de la UI
        self.setup_ui_components()
        self.setup_event_handlers()
        
        # Actualización inicial de listas
        self.update_projects_list()
        
        # Variable para mantener el proyecto actualmente seleccionado
        self.current_selected_project = None
        
        # Mostrar tareas del primer proyecto al iniciar
        if self.project_manager.projects:
            first_project = self.project_manager.projects[0]
            self.current_selected_project = first_project
            self.project_dropdown.value = first_project["name"]
            self.update_task_list(self.task_manager.get_filtered_tasks(first_project["name"]))
        else:
            self.update_task_list()
        
        # Añadir contenido a la página
        self.page.add(
            ft.Row([
                self.projects_container,
                self.tasks_tabs
            ], expand=True)
        )
    
    def setup_ui_components(self):
        """Configura los componentes de la interfaz de usuario"""
        # Referencias y componentes de la interfaz
        self.current_project = ft.Ref[ft.Dropdown]()
        self.task_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.completed_task_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.projects_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Creación del pie de página
        self.footer = ft.Container(
            content=ft.Text("Curso Algoritmia para Desarrollo de Programas\n Alumnos: Eleazar Cordero, Robert Salas",
                            size=9, color="white"),
            alignment=ft.alignment.bottom_center,
            padding=5,
            expand=True
        )
        
        # Componentes para proyectos
        self.setup_project_components()
        
        # Componentes para tareas
        self.setup_task_components()
        
        # Crear contenedores principales
        self.create_main_containers()
    
    def setup_project_components(self):
        """Configura los componentes específicos de proyectos"""
        # Campos de entrada para proyectos
        self.project_name = ft.TextField(
            label="Nombre del Proyecto",
            expand=2,
            bgcolor="#1E1E1E",
            color="white",
            border_radius=10,
            text_size=12
        )
        
        # Botón para añadir proyecto
        self.add_project_button = ft.ElevatedButton(
            "Añadir Proyecto",
            bgcolor="#6200EE",
            color="white",
            style=ft.ButtonStyle(padding=5)
        )
        
        # Dropdown de proyectos
        self.project_dropdown = ft.Dropdown(
            ref=self.current_project,
            label="Proyecto",
            options=self.project_manager.get_project_options(),
            bgcolor="#1E1E1E",
            color="white",
            width=200,
            border_radius=10,
            text_size=12,
            label_style=ft.TextStyle(size=13)
        )
    
    def setup_task_components(self):
        """Configura los componentes específicos de tareas"""
        # Campos de entrada para tareas
        self.task_name = ft.TextField(
            label="Nombre de la tarea",
            expand=2,
            bgcolor="#1E1E1E",
            color="white",
            border_radius=10,
            text_size=12,
            label_style=ft.TextStyle(size=13)
        )
        
        self.task_desc = ft.TextField(
            label="Descripción",
            expand=2,
            bgcolor="#1E1E1E",
            color="white",
            border_radius=10,
            text_size=12,
            label_style=ft.TextStyle(size=13)
        )
        
        # Selector de fecha
        self.task_date_picker = ft.DatePicker()
        
        # Botón de calendario
        self.task_date_button = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            icon_color="white",
            icon_size=15
        )
        
        # Dropdown de prioridad
        self.task_priority = ft.Dropdown(
            label="Prioridad",
            options=[
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Media"),
                ft.dropdown.Option("Baja")
            ],
            bgcolor="#1E1E1E",
            color="white",
            width=200,
            border_radius=10,
            text_size=12,
            label_style=ft.TextStyle(size=13)
        )
        
        # Campo para asignar responsable
        self.task_assigned = ft.TextField(
            label="Responsable",
            expand=1,
            bgcolor="#1E1E1E",
            color="white",
            border_radius=10,
            text_size=12,
            label_style=ft.TextStyle(size=13)
        )
        
        # Botón para añadir tarea
        self.add_button = ft.ElevatedButton(
            "Añadir",
            bgcolor="#6200EE",
            color="white",
            style=ft.ButtonStyle(padding=5)
        )
        
        self.page.overlay.append(self.task_date_picker)
    
    def create_main_containers(self):
        """Crea los contenedores principales de la aplicación"""
        # Pestañas de tareas
        self.tasks_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Tareas Pendientes",
                    content=ft.Column([
                        ft.Container(height=10),
                        ft.Row([self.task_name, self.task_date_button, self.task_priority, self.project_dropdown], spacing=10),
                        ft.Row([self.task_desc, self.task_assigned, self.add_button], spacing=10),
                        self.task_list
                    ])
                ),
                ft.Tab(
                    text="Tareas Completadas",
                    content=self.completed_task_list
                )
            ],
            expand=True
        )
        
        # Contenedor de proyectos
        self.projects_container = ft.Container(
            content=ft.Column([
                # Logo Senati centrado
                ft.Row([
                    ft.Image(
                        src="logoSenati.png",
                        width=150,
                        height=75,
                        fit=ft.ImageFit.CONTAIN
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Proyectos", size=12, color="white", weight=ft.FontWeight.BOLD),
                ft.Row([self.project_name, self.add_project_button], spacing=5),
                self.projects_list,
                self.footer
            ],
                width=300,
                alignment=ft.MainAxisAlignment.START),
            bgcolor="#1A1A1A",
            padding=10,
            border_radius=10,
            width=300
        )
    
    def setup_event_handlers(self):
        """Configura los manejadores de eventos"""
        self.add_project_button.on_click = self.handle_add_project
        self.task_date_button.on_click = self.handle_open_date_picker
        self.add_button.on_click = self.handle_add_task
    
    def update_projects_list(self):
        """Actualiza la lista de proyectos en la UI"""
        self.projects_list.controls.clear()
        
        named_projects, unnamed_project = self.project_manager.get_sorted_projects()
        
        # Añadir proyectos con nombre
        for project in named_projects:
            project_item = ft.Container(
                content=ft.Row([
                    ft.Text(project["name"], expand=True, color="white", size=12),
                    ft.IconButton(ft.icons.DELETE, icon_color="red",
                                  on_click=lambda e, p=project: self.handle_delete_project(p),
                                  icon_size=14)
                ]),
                bgcolor="#2A2A2A",
                border_radius=10,
                padding=5,
                margin=3,
                on_click=lambda e, p=project: self.handle_select_project(p)
            )
            self.projects_list.controls.append(project_item)
        
        # Añadir proyecto sin nombre al final
        for project in unnamed_project:
            project_item = ft.Container(
                content=ft.Row([
                    ft.Text(project["name"], expand=True, color="gray", size=12),
                    ft.IconButton(ft.icons.DELETE, icon_color="red",
                                  on_click=lambda e, p=project: self.handle_delete_project(p),
                                  icon_size=15)
                ]),
                bgcolor="#2A2A2A",
                border_radius=10,
                padding=5,
                margin=3,
                on_click=lambda e, p=project: self.handle_select_project(p)
            )
            self.projects_list.controls.append(project_item)
        
        # Actualizar dropdown de proyectos
        self.project_dropdown.options = self.project_manager.get_project_options()
        self.page.update()
    
    def update_task_list(self, filtered_tasks=None):
        """Actualiza la lista de tareas en la UI"""
        self.task_list.controls.clear()
        self.completed_task_list.controls.clear()
        
        # Obtener y ordenar tareas
        display_tasks = filtered_tasks if filtered_tasks is not None else self.task_manager.tasks
        sorted_tasks = self.task_manager.get_sorted_tasks(display_tasks)
        
        for task in sorted_tasks:
            task_row = self.create_task_row(task)
            
            # Separar tareas completadas y pendientes
            if task.get("completed", False):
                self.completed_task_list.controls.append(task_row)
            else:
                self.task_list.controls.append(task_row)
        
        self.page.update()
    
    def create_task_row(self, task):
        """Crea una fila de tarea para la UI"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    # Checkbox para marcar como completada
                    ft.Checkbox(
                        value=task.get("completed", False),
                        on_change=lambda e, t=task: self.handle_toggle_complete(t)
                    ),
                    ft.Text(task["name"], expand=1, color="white", size=13),
                    ft.Text(task.get("due_date", "Sin fecha"), color="white", size=12),
                    ft.Text(task["priority"], color="yellow" if task["priority"] == "Alta" else "white", size=12),
                    # Botón para editar tarea
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, t=task: self.handle_edit_task(t), icon_color="blue",
                                  icon_size=17),
                    # Botón para eliminar tarea
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, t=task: self.handle_delete_task(t), icon_color="red",
                                  icon_size=17)
                ]),
                ft.Row([
                    ft.Text(f"Descripción: {task.get('description', '-')}", color="gray", expand=True, size=12),
                    ft.Text(f"Responsable: {task.get('assigned_to', 'No asignado')}", color="gray", size=12)
                ])
            ]),
            bgcolor="#2A2A2A",
            border_radius=10,
            padding=10,
            margin=5,
            expand=True
        )
    
    # Manejadores de eventos
    def handle_add_project(self, e):
        """Maneja el evento de añadir proyecto"""
        if self.project_name.value.strip():
            if self.project_manager.add_project(self.project_name.value):
                self.project_name.value = ""
                self.update_projects_list()
    
    def handle_delete_project(self, project):
        """Maneja el evento de eliminar proyecto"""
        if self.project_manager.delete_project(project):
            self.update_projects_list()
            self.page.update()
    
    def handle_select_project(self, project):
        """Maneja el evento de seleccionar proyecto"""
        self.current_selected_project = project
        self.project_dropdown.value = project["name"]
        filtered_tasks = self.task_manager.get_filtered_tasks(project["name"])
        self.update_task_list(filtered_tasks)
        self.page.update()
    
    def handle_add_task(self, e):
        """Maneja el evento de añadir tarea"""
        if self.task_name.value.strip():
            new_task = {
                "name": self.task_name.value,
                "description": self.task_desc.value,
                "due_date": self.task_date_picker.value.strftime("%Y-%m-%d") if self.task_date_picker.value else "Sin fecha",
                "priority": self.task_priority.value,
                "assigned_to": self.task_assigned.value,
                "project": self.project_dropdown.value or "Sin Proyecto",
                "completed": False
            }
            self.task_manager.add_task(new_task)
            self.update_task_list()
            # Limpiar campos después de añadir
            self.task_name.value = ""
            self.task_desc.value = ""
            self.task_date_picker.value = None
            self.page.update()
    
    def handle_delete_task(self, task):
        """Maneja el evento de eliminar tarea"""
        self.task_manager.delete_task(task)
        self.update_task_list()
    
    def handle_edit_task(self, task):
        """Maneja el evento de editar tarea"""
        # Llenar campos con datos de la tarea a editar
        self.task_name.value = task["name"]
        self.task_desc.value = task.get("description", "")
        self.task_date_picker.value = datetime.strptime(task.get("due_date", "Sin fecha"), "%Y-%m-%d") if task.get(
            "due_date", "Sin fecha") != "Sin fecha" else None
        self.task_priority.value = task["priority"]
        self.task_assigned.value = task.get("assigned_to", "")
        self.project_dropdown.value = task.get("project", "Sin Proyecto")
        self.task_manager.delete_task(task)
        self.update_task_list()
    
    def handle_toggle_complete(self, task):
        """Maneja el evento de marcar/desmarcar tarea como completada"""
        self.task_manager.toggle_complete(task)
        
        # Mantener el filtro de proyecto actual
        if self.current_selected_project:
            filtered_tasks = self.task_manager.get_filtered_tasks(self.current_selected_project["name"])
            self.update_task_list(filtered_tasks)
        else:
            self.update_task_list()
    
    def handle_open_date_picker(self, e):
        """Maneja el evento de abrir selector de fecha"""
        self.task_date_picker.open = True
        self.page.update()