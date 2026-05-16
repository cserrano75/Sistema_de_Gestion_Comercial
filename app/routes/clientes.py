# Aqui se maneja todo el ciclo de vida de un cliente (Leer, Crear, Actualizar y Borrar)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database
from auth import obtener_usuario_actual

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[schemas.ClienteResponse])
def get_clientes(
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual) # Mantenemos la seguridad activa
):
    # Trae todos los clientes registrados en el sistema de forma global
    return db.query(models.Cliente).all()

@router.post("/", response_model=schemas.ClienteResponse)
def crear_cliente(
    cliente: schemas.ClienteCreate, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)
):
    # Verificamos si el RUT ya existe para no duplicar empresas
    db_cliente = db.query(models.Cliente).filter(models.Cliente.rut == cliente.rut).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El RUT de este cliente ya se encuentra registrado")

    datos_cliente = cliente.model_dump()
    
    # Quitamos por completo la inyección de usuario_id para que no choque con models.py
    nuevo_cliente = models.Cliente(**datos_cliente)
    
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

# Agregamos la ruta con y sin barra para evitar conflictos de redirección en FastAPI
@router.put("/{cliente_id}", response_model=schemas.ClienteResponse)
def actualizar_cliente(
    cliente_id: int,
    cliente_actualizado: schemas.ClienteCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)
):
    # 1. Buscar si el cliente existe
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # 2. Reemplazar los campos asegurando que si viene None o vacío se guarde limpio
    db_cliente.rut = cliente_actualizado.rut
    db_cliente.nombre = cliente_actualizado.nombre if hasattr(cliente_actualizado, 'nombre') else cliente_actualizado.razon_social
    db_cliente.razon_social = cliente_actualizado.razon_social
    db_cliente.giro = cliente_actualizado.giro if cliente_actualizado.giro else ""
    db_cliente.direccion = cliente_actualizado.direccion if cliente_actualizado.direccion else ""

    # 3. Guardar cambios en la base de datos
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente