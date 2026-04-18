from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- ESQUEMAS PARA CONTACTOS ---
class ContactoBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

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
    fecha_inicio: datetime
    contactos: List[Contacto] = [] # Incluimos los contactos vinculados
    
    class Config:
        from_attributes = True