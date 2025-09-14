import json
import os
from config import ARCHIVO_DATOS

def cargar_servicios():
    """Carga los servicios desde el JSON."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return {}

def guardar_servicios(data):
    """Guarda los servicios en el JSON."""
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(data, f, indent=4)

def agregar_historial(servicios, usuario_id, segundos):
    """
    Agrega el tiempo de servicio completado al historial del usuario.
    """
    if usuario_id not in servicios:
        servicios[usuario_id] = []
    servicios[usuario_id].append(segundos)
    guardar_servicios(servicios)
