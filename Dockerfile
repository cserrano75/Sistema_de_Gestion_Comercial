FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Le decimos que la raíz de búsqueda es /code
ENV PYTHONPATH=/code 

WORKDIR /code

# Dependencias para PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copiamos los requerimientos y los instalamos
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiamos toda la carpeta app al contenedor
COPY ./app /code/app

# Comando de inicio usando el paquete app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]