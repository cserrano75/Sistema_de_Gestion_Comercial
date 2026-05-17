from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, proyectos, clientes, bitacora

# Borramos el 'import models' viejo y dejamos solo este:
from app import models, database 

# 1. Crear las tablas usando las referencias correctas
models.Base.metadata.create_all(bind=database.engine)

# === 🚀 INYECCIÓN DIRECTA DE EMERGENCIA (EVITA SCRIPTS EXT) ===
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_temporal = SessionLocal()
try:
    correo_emergencia = "claudio.serrano.rojas@gmail.com"
    # Borramos cualquier rastro corrupto que el backend tenga en SU base de datos real
    db_temporal.query(User).filter(User.email == correo_emergencia).delete()
    db_temporal.commit()
    
    # Creamos el usuario fresco con la clave correcta usando la encriptación directa del backend
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
# =============================================================

# 2. Inicializar la App desactivando redirección de barras diagonales
app = FastAPI(title="CRM Industrial API", redirect_slashes=False)

# 3. Configuración robusta de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sistema-de-gestion-comercial-pi.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mantenemos el comodín temporal para saltar el bloqueo en Vercel/Render
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