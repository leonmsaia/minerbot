# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY requirements.txt .
COPY bot.py .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta el bot
CMD ["python", "bot.py"]
