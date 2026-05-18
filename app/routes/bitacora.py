# app/routes/bitacora.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import obtener_usuario_actual

router = APIRouter(prefix="/bitacora", tags=["Bitácora"])

@router.get("/{proyecto_id}", response_model=list[schemas.BitacoraResponse]) # 👈 ¡Le quitamos la barra final '/'!
def get_bitacora(
    proyecto_id: int, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)
):
    # Buscamos el proyecto globalmente solo por su ID único
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
    return db.query(models.Bitacora).filter(models.Bitacora.proyecto_id == proyecto_id).all()

@router.post("/", response_model=schemas.BitacoraResponse)
def crear_entrada_bitacora(
    entrada: schemas.BitacoraCreate, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)
):
    # CORREGIDO: Buscamos el proyecto globalmente solo por su ID único sin colapsar por 'usuario_id'
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == entrada.proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    datos_entrada = entrada.model_dump()
    if hasattr(models.Bitacora, 'usuario_id'):
        datos_entrada["usuario_id"] = current_user.id

    nueva_entrada = models.Bitacora(**datos_entrada)
    db.add(nueva_entrada)
    
    # Sincronizamos el estado si el frontend envía una actualización
    if hasattr(entrada, 'estado_nuevo') and entrada.estado_nuevo:
        proyecto.estado = entrada.estado_nuevo 
    elif hasattr(entrada, 'estado_proyecto') and entrada.estado_proyecto: # Por si usa este nombre en el esquema
        proyecto.estado = entrada.estado_proyecto

    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada