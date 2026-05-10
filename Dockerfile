FROM python:3.11-slim

# Configuraciones de Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Importante: Ponemos el directorio actual en el path
ENV PYTHONPATH=/code/app

WORKDIR /code

# Instalación de dependencias del sistema
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copiamos los archivos de la carpeta app a la raíz del contenedor
COPY ./app /code/app

# Instalamos las librerías desde la nueva ubicación
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

# El comando de inicio ahora es directo, sin el prefijo "app."
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]