import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del bot
TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "!"
CANAL_SERVICIO = 1416555773970088104  # Cambia por el ID de tu canal
ARCHIVO_DATOS = "servicios.json"
ROL_SERVICIO = "En Servicio"
