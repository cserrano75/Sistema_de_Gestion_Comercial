import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"La URL cargada es: {DATABASE_URL}") # <--- Agrega esto para ver qué está leyendo

engine = create_engine(
    DATABASE_URL, 
    connect_args={"options": "-c client_encoding=utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Esta función la usaremos en las rutas para abrir/cerrar la conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()