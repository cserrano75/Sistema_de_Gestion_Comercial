ffrom sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cliente = Column(String) # Empresa principal
    
    # --- NUEVOS CAMPOS DE GESTIÓN ---
    estado = Column(String, default="Prospecto") # Prospecto, Cotización, Ejecución, Finalizado, Perdido
    presupuesto = Column(Float, default=0.0)
    prioridad = Column(String, default="Media") # Alta, Media, Baja
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_entrega_estimada = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    eventos = relationship("Bitacora", back_populates="proyecto")
    contactos = relationship("Contacto", back_populates="proyecto")

class Contacto(Base):
    __tablename__ = "contactos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    cargo = Column(String)
    email = Column(String)
    telefono = Column(String)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))

    # Relación inversa
    proyecto = relationship("Proyecto", back_populates="contactos")

class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    tipo_entrada = Column(String) # Texto, Voz, Email
    contenido = Column(String)
    accion_pendiente = Column(Boolean, default=False)

    # Relación inversa
    proyecto = relationship("Proyecto", back_populates="eventos")