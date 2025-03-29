import json

class DataManager:
    """Clase para manejar la persistencia de datos"""
    
    @staticmethod
    def load_data(filename, default=None):
        """
        Carga datos desde un archivo JSON.
        Si el archivo no existe, devuelve un valor por defecto.
        """
        try:
            with open(filename, "r",encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default or []
    
    @staticmethod
    def save_data(data, filename):
        """
        Guarda datos en un archivo JSON.
        """
        with open(filename, "w",encoding="utf-8") as f:
            json.dump(data, f)