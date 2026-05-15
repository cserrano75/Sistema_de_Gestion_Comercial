# app/routes/bitacora.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, database, schemas
from auth import obtener_usuario_actual

router = APIRouter(prefix="/bitacora", tags=["Bitácora"])

@router.get("/{proyecto_id}", response_model=list[schemas.BitacoraResponse])
def get_bitacora(
    proyecto_id: int, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)  # <-- Limpio
):
    proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id == proyecto_id, 
        models.Proyecto.usuario_id == current_user.id
    ).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado o no autorizado")
    return db.query(models.Bitacora).filter(models.Bitacora.proyecto_id == proyecto_id).all()

@router.post("/", response_model=schemas.BitacoraResponse)
def crear_entrada_bitacora(
    entrada: schemas.BitacoraCreate, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)  # <-- Limpio
):
    proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id == entrada.proyecto_id,
        models.Proyecto.usuario_id == current_user.id
    ).first()
    if not proyecto:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este proyecto")

    datos_entrada = entrada.model_dump()
    if hasattr(models.Bitacora, 'usuario_id'):
        datos_entrada["usuario_id"] = current_user.id

    nueva_entrada = models.Bitacora(**datos_entrada)
    db.add(nueva_entrada)
    if entrada.estado_nuevo:
        proyecto.estado = entrada.estado_nuevo 
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada