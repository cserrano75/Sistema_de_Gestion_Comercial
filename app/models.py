# *******************************************************************************
# En este archivo es donde definimos las reglas de cómo se guarda la información 
# en la base de datos de forma permanente
# *******************************************************************************

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text # <--- Importamos Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True)
    razon_social = Column(String, index=True)
    giro = Column(String)
    direccion = Column(String)
    
    # Un cliente puede tener muchos proyectos asociados
    proyectos = relationship("Proyecto", back_populates="cliente")

# app/models.py
class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    presupuesto = Column(Float)
    
    # Ajustamos el estado inicial a tu nuevo flujo
    estado = Column(String, default="Lead o Prospecto") 
    
    # RELACIONES
    cliente = relationship("Cliente", back_populates="proyectos")
    contactos = relationship("Contacto", back_populates="proyecto")
    # Usamos 'bitacoras' para que el frontend reciba los datos correctamente
    bitacoras = relationship("Bitacora", back_populates="proyecto")

class Contacto(Base):
    __tablename__ = "contactos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    cargo = Column(String)
    email = Column(String)
    telefono = Column(String)
    
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    proyecto = relationship("Proyecto", back_populates="contactos")

class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    tipo_entrada = Column(String)  # Llamada, Reunión, etc.
    contenido = Column(Text)
    # NUEVO: Guardamos si esta entrada cambió el estado del proyecto
    estado_nuevo = Column(String, nullable=True) 
    fecha_registro = Column(DateTime, default=func.now())

    proyecto = relationship("Proyecto", back_populates="bitacoras")