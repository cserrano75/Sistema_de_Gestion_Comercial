from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# CAMBIO AQUÍ: Importaciones absolutas
from app import models, schemas, database
from app.auth import obtener_usuario_actual

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


# --- SECCIÓN 1: GESTIÓN DE PROYECTOS ---
# quedan con error

@router.get("/", response_model=list[schemas.ProyectoResponse])
def leer_lista_proyectos(
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)  # Mantiene la seguridad activa
):
    # Trae absolutamente todos los proyectos de forma global
    return db.query(models.Proyecto).all()

@router.post("/", response_model=schemas.ProyectoResponse)
def crear_nuevo_proyecto(
    proyecto: schemas.ProyectoCreate, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)  # <-- Aquí también
):
    datos_proyecto = proyecto.model_dump()
    # datos_proyecto["usuario_id"] = current_user.id
    nuevo_proyecto = models.Proyecto(**datos_proyecto)
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto

# --- SECCIÓN 2: ESTADÍSTICAS ---
# IMPORTANTE: Solo dejamos UNA versión de esta función

@router.get("/stats/resumen")
def obtener_estadisticas(db: Session = Depends(database.get_db)):
    proyectos = db.query(models.Proyecto).all()
    total = len(proyectos)
    
    if total == 0:
        return {
            "monto_adjudicado": 0, "monto_en_estudio": 0, "monto_perdido": 0,
            "tasa_conversion": 0, "total_proyectos": 0
        }

    adjudicados = [p for p in proyectos if p.estado == "Adjudicado"]
    estudio = [p for p in proyectos if p.estado in ["Estudio", "Cotizado"]]
    perdidos = [p for p in proyectos if p.estado == "Perdido"]

    return {
        "monto_adjudicado": sum(p.presupuesto for p in adjudicados),
        "monto_en_estudio": sum(p.presupuesto for p in estudio),
        "monto_perdido": sum(p.presupuesto for p in perdidos),
        "tasa_conversion": round((len(adjudicados)/total*100), 1),
        "total_proyectos": total
    }

# --- SECCIÓN 3: BITÁCORA ---

@router.post("/bitacora", response_model=schemas.BitacoraResponse)
def agregar_entrada_bitacora(
    entrada: schemas.BitacoraCreate, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual) # 1. Forzamos la sesión del usuario logueado
):
    # 2. Verificar que el proyecto exista
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == entrada.proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # 3. Construir la entrada sanitizando vacíos para que no rompa Pydantic
    nueva_entrada = models.Bitacora(
        proyecto_id=entrada.proyecto_id,
        tipo_contacto=entrada.tipo_contacto if entrada.tipo_contacto else "Llamada",
        detalle=entrada.detalle.strip() if entrada.detalle else "",
        estado_proyecto=entrada.estado_proyecto if entrada.estado_proyecto else proyecto.estado,
        usuario_id=current_user.id # Inyectamos el ID del usuario que inició sesión
    )
    
    # 4. Sincronizar: Actualizamos el estado actual del proyecto principal
    if entrada.estado_proyecto:
        proyecto.estado = entrada.estado_proyecto

    db.add(nueva_entrada)
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada

@router.get("/{proyecto_id}/bitacora", response_model=list[schemas.BitacoraResponse])
def obtener_bitacora_proyecto(
    proyecto_id: int, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual) # Protegemos también la lectura
):
    """Busca el historial de un proyecto específico"""
    return db.query(models.Bitacora).filter(models.Bitacora.proyecto_id == proyecto_id).all()