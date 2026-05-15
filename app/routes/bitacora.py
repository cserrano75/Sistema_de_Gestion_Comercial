# app/routes/bitacora.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas, database
from auth import obtener_usuario_actual

router = APIRouter(prefix="/bitacora", tags=["Bitácora"])

get_db = database.get_db

@router.get("/{proyecto_id}", response_model=list[schemas.BitacoraResponse])
def get_bitacora(
    proyecto_id: int, 
    db: Session = Depends(database.get_db),
    current_user: str = Depends(obtener_usuario_actual) # <--- EL CANDADO
):
    return db.query(models.Bitacora).filter(models.Bitacora.proyecto_id == proyecto_id).all()

@router.post("/", response_model=schemas.BitacoraResponse)
def crear_entrada_bitacora(
    entrada: schemas.BitacoraCreate, 
    db: Session = Depends(database.get_db),
    current_user: str = Depends(obtener_usuario_actual) # <--- EL CANDADO
):
    # Tu lógica actual de guardado...
    nueva_entrada = models.Bitacora(**entrada.dict())
    db.add(nueva_entrada)
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada

@router.post("/", response_model=schemas.Bitacora)
def crear_entrada(entrada: schemas.BitacoraCreate, db: Session = Depends(get_db)):
    # 1. Crear el registro de la bitácora
    nueva_entrada = models.Bitacora(**entrada.model_dump())
    db.add(nueva_entrada)
    
    # 2. Lógica de cambio de estado:
    # Si el usuario seleccionó un nuevo estado en el panel lateral...
    if entrada.estado_nuevo:
        proyecto = db.query(models.Proyecto).filter(
            models.Proyecto.id == entrada.proyecto_id
        ).first()
        
        if proyecto:
            proyecto.estado = entrada.estado_nuevo # <--- Aquí ocurre la magia
    
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada