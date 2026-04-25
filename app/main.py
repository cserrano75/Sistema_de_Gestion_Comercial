from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import proyectos, clientes
from . import models, database

# Creamos las tablas en la BD
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="CRM Industrial API")

# --- CONFIGURACIÓN DE SEGURIDAD (CORS) ---
# Esto permite que tu Frontend (puerto 5173) le pida datos al Backend (puerto 8000)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# Registramos las rutas
app.include_router(proyectos.router)
app.include_router(clientes.router) # Activa el maestro de clientes

@app.get("/")
def home():
    return {"mensaje": "Bienvenido al API del CRM Industrial"}