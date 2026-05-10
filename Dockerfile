# Usamos una imagen de Python oficial y ligera
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH=/code
# Directorio de trabajo dentro del contenedor
WORKDIR /code

# Instalamos dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copiamos solo el requirements.txt primero para aprovechar el cache de Docker
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiamos TODO el contenido de la carpeta app al directorio /code/app
COPY ./app /code/app

# Comando final para arrancar la app
# Nota: Usamos "app.main:app" porque estamos parados en /code y la carpeta se llama app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]