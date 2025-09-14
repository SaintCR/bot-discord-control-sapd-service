import os
from dotenv import load_dotenv

# ---------------- CARGAR VARIABLES DE ENTORNO ----------------
load_dotenv()

# ---------------- CONFIGURACIÓN DEL BOT ----------------
TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "!"
CANAL_SERVICIO = 1416555773970088104  # ID del canal donde se usa !servicio
CANAL_TOP_DOMINGO = 1416803772667133962  # ID del canal donde se publicará el top semanal
ARCHIVO_DATOS = "servicios.json"
ROL_SERVICIO = "En Servicio"
