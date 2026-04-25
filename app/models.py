# *******************************************************************************
# En este archivo es donde definimos las reglas de cómo se guarda la información 
# en la base de datos de forma permanente
# *******************************************************************************

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
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

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    
    # CONEXIÓN: El proyecto ahora pertenece a un Cliente ID
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    presupuesto = Column(Float)
    estado = Column(String, default="Cotización")
    
    # RELACIONES
    cliente = relationship("Cliente", back_populates="proyectos")
    contactos = relationship("Contacto", back_populates="proyecto")
    eventos = relationship("Bitacora", back_populates="proyecto")

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
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    tipo_entrada = Column(String) 
    contenido = Column(String)
    accion_pendiente = Column(Boolean, default=False)
    
    proyecto = relationship("Proyecto", back_populates="eventos")