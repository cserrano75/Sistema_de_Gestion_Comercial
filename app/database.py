import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Obtenemos la URL (Prioridad a la variable de entorno de Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Seguridad: Si no hay URL, usamos una de emergencia o lanzamos error claro
if not DATABASE_URL:
    # Esto evitará que la app intente arrancar si la variable está vacía
    print("CRITICAL: DATABASE_URL is not set!")
    # Solo para que no explote el engine si falta la variable durante el build
    DATABASE_URL = "sqlite:///./test.db" 

# 3. Corrección automática (postgres -> postgresql)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Configuración del Engine
# Simplificamos connect_args para evitar conflictos de SSL en Render
connect_args = {}
if "postgresql" in DATABASE_URL:
    connect_args = {"options": "-c client_encoding=utf8"}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()