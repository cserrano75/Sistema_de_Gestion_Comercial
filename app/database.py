import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# 1. Obtenemos la URL de la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Corrección automática para Render/Heroku (postgres -> postgresql)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Configuración del Engine
# Añadimos un chequeo para SSL que Render suele requerir
connect_args = {"options": "-c client_encoding=utf8"}
if DATABASE_URL and "localhost" not in DATABASE_URL:
    # Esto le dice a SQLAlchemy que use una conexión segura en la nube
    connect_args["sslmode"] = "require"

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()