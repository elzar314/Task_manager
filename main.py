import flet as ft
from ui.task_app import TaskApp

def main(page: ft.Page):
    """Función principal para iniciar la aplicación"""
    app = TaskApp(page)

# Iniciar la aplicación
if __name__ == "__main__":
    ft.app(target=main)