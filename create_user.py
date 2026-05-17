import sys
from os.path import dirname, abspath

# Esto evita errores de rutas agregando la carpeta raíz al sistema
sys.path.insert(0, dirname(abspath(__file__)))

from app.database import SessionLocal
from app.models import User  # <-- Cambiado a User de forma definitiva
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_usuario_inicial():
    db = SessionLocal()
    try:
        email_buscar = "claudio.serrano.rojas@gmail.com"
        
        # Verificar si ya existe por si acaso
        db_user = db.query(User).filter(User.email == email_buscar).first()
        if db_user:
            print(f"El usuario {email_buscar} ya existe en esta base de datos.")
            return

        # Creamos usando la clase 'User'
        hashed_password = pwd_context.hash("csr2026") # <-- Recuerda poner tu clave real aquí
        nuevo_usuario = User(
            email=email_buscar,
            hashed_password=hashed_password,
            nombre="Claudio Serrano",
            is_active=True
        )
        
        db.add(nuevo_usuario)
        db.commit()
        print(f"¡Usuario {email_buscar} creado con éxito en la base de datos de Codespaces!")
    except Exception as e:
        print(f"Hubo un error al crear el usuario: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario_inicial()