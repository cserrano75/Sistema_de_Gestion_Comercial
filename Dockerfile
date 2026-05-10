FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Le decimos a Python que su casa es la carpeta /app
ENV PYTHONPATH=/app 

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copiamos los requerimientos desde tu carpeta local app
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPIAMOS TODO EL CONTENIDO DE TU CARPETA APP DIRECTO A LA RAÍZ DEL CONTENEDOR
COPY ./app/ .

# El comando ahora es directo al grano
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]