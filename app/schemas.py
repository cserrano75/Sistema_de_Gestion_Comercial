# Aquí definiremos qué datos aceptamos del exterior. 
# Esto previene que alguien intente enviar campos maliciosos a la base de datos.
# Los Schemas son solo para validar la entrada y salida de datos por internet. 
# No tocan la base de datos directamente.

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# NOTA: Estos son como los 'User-Defined Types' (UDT) de VB6.
# Sirven para que el sistema sepa qué campos esperar del Frontend.

# --- ESQUEMAS DE CONTACTOS ---
class ContactoBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    proyecto_id: int

class ContactoCreate(ContactoBase):
    pass # Se usa para el 'INSERT'

class Contacto(ContactoBase):
    id: int # El 'ID' lo devuelve la BD, no lo envía el usuario
    class Config:
        from_attributes = True

# --- ESQUEMAS DE BITÁCORA ---
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

# --- ESQUEMAS DE PROYECTO ---
class ProyectoBase(BaseModel):
    nombre: str
    cliente: str
    presupuesto: float
    estado: str = "Cotización"

class ProyectoCreate(ProyectoBase):
    pass

class Proyecto(ProyectoBase):
    id: int
    # Relaciones: Esto permite que al consultar un proyecto, 
    # FastAPI traiga automáticamente su gente y sus notas.
    contactos: List[Contacto] = []
    eventos: List[Bitacora] = [] 

    class Config:
        from_attributes = True



class ClienteBase(BaseModel):
    rut: str
    razon_social: str
    giro: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    class Config:
        from_attributes = True

# Actualiza también el esquema de Proyecto para que acepte cliente_id
class ProyectoCreate(BaseModel):
    nombre: str
    cliente_id: int  # Ahora esperamos el ID numérico del cliente
    presupuesto: float
    estado: Optional[str] = "Cotización"