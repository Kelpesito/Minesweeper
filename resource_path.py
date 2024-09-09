################################################################################
############## Función para obtener la ruta absoluta de un archivo #############
################################################################################


import os
import sys


def resource_path(relative_path):
    """
    Parámetro:
    ----------
    relative_path: str
        Ruta relativa de un archivo
    ----------
    Devuelve:
    ---------
    str = os.path.join(base_path, relative_path)
        Ruta absoluta de un archivo
    ---------
    Get absolute path to resource, works for dev and for PyInstaller
    """
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
