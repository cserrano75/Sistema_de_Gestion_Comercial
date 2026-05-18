from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

# Importaciones de tu CRM
from app import models, database 
from app.database import SessionLocal
from app.models import User
from app.routes import auth_routes, proyectos, clientes, bitacora

# 1. Crear las tablas usando las referencias correctas
models.Base.metadata.create_all(bind=database.engine)

# 2. Inicializar la App desactivando redirección de barras diagonales
app = FastAPI(title="CRM Industrial API", redirect_slashes=False)

# 3. Configuración Robusta de CORS para Codespaces - original
""" origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sistema-de-gestion-comercial-pi.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origin_regex=r"https://.*\.app\.github\.dev",  # Autoriza dinámicamente cualquier puerto proxy de tu GitHub
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """

# # 3. Configuración Robusta de CORS para Codespaces - propuesta
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sistema-de-gestion-comercial-pi.vercel.app",
    "https://cuddly-space-parakeet-jj65xpp75pvh5qvp-5173.app.github.dev",  # 👈 Tu frontend actual
    "https://cuddly-space-parakeet-jj65xpp75pvh5qvp-8000.app.github.dev"   # 👈 Tu backend actual
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 👈 Usamos la lista explícita segura
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 🚀 INYECCIÓN DIRECTA DE EMERGENCIA (Falta en tu archivo actual) ===
db_temporal = SessionLocal()
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    correo_emergencia = "claudio.serrano.rojas@gmail.com"
    
    # Limpiamos registros huérfanos o corruptos
    db_temporal.query(User).filter(User.email == correo_emergencia).delete()
    db_temporal.commit()
    
    # Insertamos tu usuario final de forma limpia con hash verificado por passlib
    user_root = User(
        email=correo_emergencia,
        hashed_password=pwd_context.hash("csr2026"),
        nombre="Claudio Serrano",
        is_active=True
    )
    db_temporal.add(user_root)
    db_temporal.commit()
    print("\n🚀 [SISTEMA] ¡USUARIO INYECTADO DIRECTAMENTE DESDE EL CORAZÓN DEL BACKEND! 🚀\n")
except Exception as e:
    print(f"\n❌ Error en la inyección interna: {e}\n")
finally:
    db_temporal.close()
# ===================================================================

# 4. Registro de rutas (Endpoints)
app.include_router(auth_routes.router)
app.include_router(proyectos.router)
app.include_router(clientes.router)
app.include_router(bitacora.router)

@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "CRM API Funcionando"}