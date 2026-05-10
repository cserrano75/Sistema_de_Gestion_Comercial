import sys
import os

# 1. PRIMERO: Configuramos las rutas (antes de importar tus módulos)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. SEGUNDO: Importaciones de librerías externas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 3. TERCERO: Importaciones de TUS archivos (ahora Python sí sabrá dónde están)
from routes import auth_routes, proyectos, clientes, bitacora
import models
import database

# 4. CUARTO: Inicialización
app = FastAPI()

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="CRM Industrial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas (Endpoints)
app.include_router(auth_routes.router) # <--- Ahora la seguridad tiene su propio lugar
app.include_router(proyectos.router)
app.include_router(clientes.router)
app.include_router(bitacora.router)

@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "CRM API Funcionando"}