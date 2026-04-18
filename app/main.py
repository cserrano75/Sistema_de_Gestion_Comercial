import os
from fastapi import FastAPI
from .database import engine, Base
from .routes import proyectos # Importamos nuestro nuevo archivo de rutas

# Creamos las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM Industrial - Claudio Serrano")

@app.get("/")
def home():
    return {"mensaje": "Bienvenido Claudio, el sistema está operando bajo arquitectura modular"}

# EL PASO CLAVE: Conectamos las rutas de proyectos al sistema principal
app.include_router(proyectos.router)