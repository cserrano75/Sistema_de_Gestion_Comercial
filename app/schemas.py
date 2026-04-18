# Aquí definiremos qué datos aceptamos del exterior. 
# Esto previene que alguien intente enviar campos maliciosos a la base de datos.

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- ESQUEMAS PARA CONTACTOS ---
class ContactoBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    proyecto_id: int

class ContactoCreate(ContactoBase):
    proyecto_id: int

class Contacto(ContactoBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS PARA PROYECTOS (Con nuevos campos de gestión) ---
class ProyectoBase(BaseModel):
    nombre: str
    cliente: str
    estado: Optional[str] = "Prospecto"
    presupuesto: Optional[float] = 0.0
    prioridad: Optional[str] = "Media"
    fecha_entrega_estimada: Optional[datetime] = None

class ProyectoCreate(ProyectoBase):
    pass

class Proyecto(ProyectoBase):
    id: int
    contactos: List[Contacto] = []
    eventos: List[Bitacora] = [] # Aquí es donde conectamos la bitácora al proyecto

    class Config:
        from_attributes = True

# --- SCHEMAS PARA BITÁCORA ---

class BitacoraBase(BaseModel):
    proyecto_id: int
    tipo_entrada: str  # Ejemplo: "Llamada", "Visita", "Email"
    contenido: str
    accion_pendiente: bool = False

class BitacoraCreate(BitacoraBase):
    pass

class Bitacora(BitacoraBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

# --- RE-DEFINICIÓN DE PROYECTO (Para incluir la bitácora en las consultas) ---

