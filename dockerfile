# Usa Python 3.12
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos de tu proyecto
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto para Flask si usas mini servidor
EXPOSE 8080

# Ejecuta tu bot
CMD ["python", "bot.py"]
