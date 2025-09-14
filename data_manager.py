import json
import os
from config import ARCHIVO_DATOS

def cargar_servicios():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return {}

def guardar_servicios(data):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(data, f, indent=4)
