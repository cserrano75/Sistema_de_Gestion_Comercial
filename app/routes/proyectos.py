from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# CAMBIO AQUÍ: Importaciones absolutas
import models, schemas, database
from auth import obtener_usuario_actual


router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


# --- SECCIÓN 1: GESTIÓN DE PROYECTOS ---
# quedan con error

@router.get("/", response_model=list[schemas.ProyectoResponse])
def leer_lista_proyectos(
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)  # <-- Le quitamos el tipado problemático
):
    return db.query(models.Proyecto).filter(models.Proyecto.usuario_id == current_user.id).all()

@router.post("/", response_model=schemas.ProyectoResponse)
def crear_nuevo_proyecto(
    proyecto: schemas.ProyectoCreate, 
    db: Session = Depends(database.get_db),
    current_user = Depends(obtener_usuario_actual)  # <-- Aquí también
):
    datos_proyecto = proyecto.model_dump()
    datos_proyecto["usuario_id"] = current_user.id
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
def agregar_entrada_bitacora(entrada: schemas.BitacoraCreate, db: Session = Depends(database.get_db)):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == entrada.proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    nueva_entrada = models.Bitacora(**entrada.model_dump())
    db.add(nueva_entrada)
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada

@router.get("/{proyecto_id}/bitacora", response_model=list[schemas.BitacoraResponse])
def obtener_bitacora_proyecto(proyecto_id: int, db: Session = Depends(database.get_db)):
    """Busca el historial de un proyecto específico"""
    return db.query(models.Bitacora).filter(models.Bitacora.proyecto_id == proyecto_id).all()