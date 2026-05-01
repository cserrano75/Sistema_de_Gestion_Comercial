from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import proyectos, clientes # Tus rutas
from . import models, database
from .routes import proyectos, clientes, bitacora # <--- Agregar bitacora

# Creamos las tablas en la BD
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
# app = FastAPI(title="CRM Industrial API")

# --- CONFIGURACIÓN DE SEGURIDAD (CORS) ---
# Esto permite que tu Frontend (puerto 5173) le pida datos al Backend (puerto 8000)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo, esto permite que cualquier origen (como localhost:5173) se conecte
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los encabezados
)

# Registramos las rutas
app.include_router(proyectos.router)
app.include_router(clientes.router) # Activa el maestro de clientes
app.include_router(bitacora.router)

@app.get("/")
def home():
    return {"mensaje": "Bienvenido al API del CRM Industrial"}