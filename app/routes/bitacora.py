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
    current_user: models.Usuario = Depends(obtener_usuario_actual) # <-- Cambiado a models.Usuario
):
    """Retorna la bitácora de un proyecto, validando que pertenezca al usuario logueado"""
    # Primero verificamos si el proyecto realmente le pertenece al usuario actual
    proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id == proyecto_id, 
        models.Proyecto.usuario_id == current_user.id
    ).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Proyecto no encontrado o no autorizado"
        )
        
    return db.query(models.Bitacora).filter(models.Bitacora.proyecto_id == proyecto_id).all()


@router.post("/", response_model=schemas.BitacoraResponse)
def crear_entrada_bitacora(
    entrada: schemas.BitacoraCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(obtener_usuario_actual) # <-- Cambiado a models.Usuario
):
    """Crea una entrada en la bitácora y actualiza el estado del proyecto si corresponde"""
    # 1. Validar que el proyecto al que se le añade la bitácora le pertenezca al usuario
    proyecto = db.query(models.Proyecto).filter(
        models.Proyecto.id == entrada.proyecto_id,
        models.Proyecto.usuario_id == current_user.id
    ).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar este proyecto"
        )

    # 2. Convertir esquema a diccionario e inyectar el usuario_id (por si la tabla bitacora lo requiere)
    datos_entrada = entrada.model_dump()
    if hasattr(models.Bitacora, 'usuario_id'):
        datos_entrada["usuario_id"] = current_user.id

    # 3. Crear el registro de la bitácora
    nueva_entrada = models.Bitacora(**datos_entrada)
    db.add(nueva_entrada)
    
    # 4. Lógica de cambio de estado (la magia del panel lateral)
    if entrada.estado_nuevo:
        proyecto.estado = entrada.estado_nuevo 
    
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada