# *******************************************************************************
# En este archivo es donde definimos las reglas de cómo se guarda la información 
# en la base de datos de forma permanente
# *******************************************************************************

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# NOTA: Este archivo define la estructura REAL en la base de datos Postgres.
# Es el equivalente a diseñar las tablas en el Relationship Manager de Access.

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cliente = Column(String)
    presupuesto = Column(Float)
    estado = Column(String, default="Cotización")
    
    # RELACIONES: 
    # 'contactos' y 'eventos' son como sub-formularios vinculados.
    # No existen como columnas en la tabla 'proyectos', sino como enlaces lógicos.
    contactos = relationship("Contacto", back_populates="proyecto")
    eventos = relationship("Bitacora", back_populates="proyecto")

class Contacto(Base):
    __tablename__ = "contactos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    cargo = Column(String)
    email = Column(String)
    telefono = Column(String)
    
    # CLAVE FORÁNEA: El ancla que lo une al proyecto.
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    
    # El camino de vuelta: permite saber a qué proyecto pertenece este contacto.
    proyecto = relationship("Proyecto", back_populates="contactos")

class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    
    # Registro automático de tiempo (para no tener que escribir la fecha a mano)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    tipo_entrada = Column(String) # Llamada, Reunión, Correo
    contenido = Column(String)
    accion_pendiente = Column(Boolean, default=False)
    
    proyecto = relationship("Proyecto", back_populates="eventos")