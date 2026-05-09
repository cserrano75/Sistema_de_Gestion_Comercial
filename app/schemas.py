# Aquí definiremos qué datos aceptamos del exterior. 
# Esto previene que alguien intente enviar campos maliciosos a la base de datos.
# Los Schemas son solo para validar la entrada y salida de datos por internet. 
# No tocan la base de datos directamente.

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# --- ESQUEMAS DE SEGURIDAD (TOKEN) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- ESQUEMAS DE USUARIO ---

class UserBase(BaseModel):
    email: EmailStr
    nombre: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

# --- ESQUEMAS DE CONTACTOS ---

class ContactoBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    proyecto_id: int

class ContactoCreate(ContactoBase):
    pass

class Contacto(ContactoBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS DE BITÁCORA ---

class BitacoraBase(BaseModel):
    proyecto_id: int
    tipo_entrada: str
    contenido: str
    estado_nuevo: Optional[str] = None

class BitacoraCreate(BitacoraBase):
    pass

class BitacoraResponse(BitacoraBase):
    id: int
    fecha_registro: datetime
    class Config:
        from_attributes = True

# Para compatibilidad, Bitacora es lo mismo que BitacoraResponse
Bitacora = BitacoraResponse

# --- ESQUEMAS DE CLIENTES ---

class ClienteBase(BaseModel):
    rut: str
    razon_social: str
    giro: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS DE PROYECTO ---

class ProyectoBase(BaseModel):
    nombre: str
    cliente_id: int 
    presupuesto: float
    estado: Optional[str] = "Cotización"

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoResponse(ProyectoBase):
    id: int
    # Relaciones: Esto permite que FastAPI traiga los datos vinculados
    contactos: List[Contacto] = []
    eventos: List[BitacoraResponse] = [] 

    class Config:
        from_attributes = True

# Este alias es VITAL para que Proyecto y ProyectoResponse funcionen como uno solo
Proyecto = ProyectoResponse