# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios desde el contexto de construcción
COPY ./src/ ./
COPY ./requirements.txt ./requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta el bot
CMD ["python", "./bot.py"]
