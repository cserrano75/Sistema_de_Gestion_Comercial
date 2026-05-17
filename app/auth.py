from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# IMPORTACIONES DE TU BASE DE DATOS Y MODELOS
from app import database, models

SECRET_KEY = "CLAVE_SUPER_SECRETA_123"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Cambiamos bcrypt por argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def obtener_password_hash(password: str):
    return pwd_context.hash(str(password))

def verificar_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(str(plain_password), hashed_password)

def crear_token_acceso(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=480)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- REFACTORIZACIÓN CONECTADA A LA BASE DE DATOS ---
def obtener_usuario_actual(
    db: Session = Depends(database.get_db), # Inyectamos la sesión de la base de datos
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Buscamos el objeto usuario real en la tabla utilizando el email del token
    usuario = db.query(models.User).filter(models.User.email == email).first()
    
    if usuario is None:
        raise credentials_exception

    # Devolvemos el objeto completo (con su .id, .nombre, etc.)
    return usuario