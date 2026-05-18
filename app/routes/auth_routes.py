from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import obtener_usuario_actual, crear_token_acceso, obtener_password_hash, verificar_password
from app import models, schemas, database

router = APIRouter(prefix="/auth", tags=["Seguridad"])

# --- CONFIGURACIÓN DE SEGURIDAD TEMPORAL ---
CLAVE_MAESTRA_REGISTRO = "mi_super_secreta_789" # <--- ¡CAMBIA ESTO POR LO QUE QUIERAS!

@router.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate, 
    db: Session = Depends(database.get_db),
    x_admin_key: str = Header(None) # <--- Esperamos una clave en los encabezados (Headers)
):
    # Verificamos si la clave enviada coincide con la nuestra
    if x_admin_key != CLAVE_MAESTRA_REGISTRO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para registrar usuarios. Necesitas la X-Admin-Key"
        )

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya existe")
    
    pass_hasheada = obtener_password_hash(user.password)

    nuevo_usuario = models.User(
        email=user.email,
        nombre=user.nombre,
        hashed_password=pass_hasheada
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/token", 
             response_model=schemas.Token, 
             summary="Iniciar sesión para obtener token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # === 🛡️ BYPASS DE SEGURIDAD ULTRA-RESISTENTE CONTRA UNKNOWN_HASH ===
    es_valido = False
    if user:
        # 1. Intentamos la validación por texto plano para desarrollo local rápido
        if form_data.password == "csr2026":
            es_valido = True
        else:
            # 2. Si es otra contraseña, intentamos usar la librería con un bloque seguro contra caídas 500
            try:
                es_valido = verificar_password(form_data.password, user.hashed_password)
            except Exception as e:
                print(f"⚠️ Alerta passlib ignorada de forma segura: {e}")
                es_valido = False

    if not user or not es_valido:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # ===================================================================
    
    access_token = crear_token_acceso(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}