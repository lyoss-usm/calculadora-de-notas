"""
Core utilities module.
Consolidated utility functions for JSON handling and data processing.
"""
import json
import numpy as np


# ========== JSON Utilities ==========

def read_json(file_path):
    """Lee un archivo JSON y retorna su contenido."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json(file_path, data):
    """Escribe datos en un archivo JSON."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_evals_arrays(evals):
    """
    Extrae arrays de nombres, notas, bools e indep de las evaluaciones.
    
    Args:
        evals: Lista de evaluaciones en formato [nombre, nota, rendida, independiente]
    
    Returns:
        tuple: (names, notas, bools, indep) como arrays de numpy
    """
    names = np.array([eval[0] for eval in evals], dtype=str)
    notas = np.array([eval[1] for eval in evals], dtype=float)
    bools = np.array([eval[2] for eval in evals], dtype=bool)
    indep = np.array([eval[3] for eval in evals], dtype=bool)

    return names, notas, bools, indep


# ========== Configuration Class ==========

class AppConfig:
    """
    Clase para manejar la configuración de datos de la aplicación.
    Lee y escribe en core/data/config.json
    """
    
    def __init__(self, config_file='core/data/config.json'):
        self.config = read_json(config_file)
        self.config_file = config_file

    def get(self, key, default=None):
        """Obtiene un valor de configuración."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Establece un valor de configuración y lo guarda."""
        self.config[key] = value
        write_json(self.config_file, self.config)

    def __str__(self):
        return str(self.config)


__all__ = ['read_json', 'write_json', 'get_evals_arrays', 'AppConfig']
