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
    
    if not user or not verificar_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # Ahora 'status' funcionará
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = crear_token_acceso(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}