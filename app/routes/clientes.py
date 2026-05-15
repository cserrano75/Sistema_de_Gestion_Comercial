# Aqui se maneja todo el ciclo de vida de un cliente (Leer, Crear, Actualizar y Borrar)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas, database
from auth import obtener_usuario_actual

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# OBTENER TODOS LOS CLIENTES
@router.get("/", response_model=list[schemas.ClienteResponse])
def get_clientes(
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(obtener_usuario_actual) # <-- Cambiado a models.Usuario
):
    """Retorna los clientes pertenecientes únicamente al usuario autenticado"""
    return db.query(models.Cliente).filter(models.Cliente.usuario_id == current_user.id).all()

@router.post("/", response_model=schemas.ClienteResponse)
def crear_cliente(
    cliente: schemas.ClienteCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(obtener_usuario_actual) # <-- Cambiado a models.Usuario
):
    """Registra un nuevo cliente asociado al usuario autenticado"""
    # Convertimos el esquema a diccionario (Pydantic v2)
    datos_cliente = cliente.model_dump()
    
    # Inyectamos el ID del usuario actual que está creando el cliente
    datos_cliente["usuario_id"] = current_user.id
    
    # Creamos el modelo con los datos que ya incluyen al dueño
    nuevo_cliente = models.Cliente(**datos_cliente)
    
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

# OBTENER UN CLIENTE ESPECÍFICO
@router.get("/{cliente_id}", response_model=schemas.ClienteResponse) # <-- CORREGIDO: Era Cliente
def leer_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

# ACTUALIZAR CLIENTE
@router.put("/{cliente_id}", response_model=schemas.ClienteResponse) # <-- CORREGIDO: Era Cliente
def actualizar_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizamos los campos
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# ELIMINAR CLIENTE
@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado con éxito"}