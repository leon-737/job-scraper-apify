# Usamos una imagen oficial y ligera de Python
FROM python:3.13-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos herramientas esenciales de compilación si fuera necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente del bot
COPY . .

# Comando por defecto al ejecutar el contenedor
CMD ["python", "main.py"]
 
