from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, proyectos, clientes, bitacora  # Volvemos al original
import models
import database

# Una Sola instancia con toda la configuración unificada
app = FastAPI(title="CRM Industrial API", redirect_slashes=False)

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

# 3. Configuramos CORS de forma segura
# Aunque tienes ["*"] (que permite todo), definamos explícitamente los orígenes
# para asegurar que Render no rechace las credenciales/tokens del localhost.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sistema-de-gestion-comercial-1.onrender.com", 
    "https://sistema-de-gestion-comercial-pi.vercel.app",  # <-- TU NUEVA URL DE VERCEL AQUÍ # <-- TU NUEVO FRONTEND EN LA NUBE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cambiado de "*" a la lista explícita para evitar conflictos con credenciales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Registro de rutas (Endpoints)
app.include_router(auth_routes.router)
app.include_router(proyectos.router)
app.include_router(clientes.router)
app.include_router(bitacora.router)

@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "CRM API Funcionando"}