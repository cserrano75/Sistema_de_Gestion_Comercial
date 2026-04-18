# *******************************************************************************
# En este archivo es donde definimos las reglas de cómo se guarda la información 
# en la base de datos de forma permanente
# *******************************************************************************

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cliente = Column(String) # Empresa principal
    
    # --- CAMPOS DE GESTIÓN COMERCIAL ---
    # Estados sugeridos: Prospecto, Cotización, Ejecución, Finalizado, Perdido
    estado = Column(String, default="Prospecto") 
    presupuesto = Column(Float, default=0.0)
    prioridad = Column(String, default="Media") # Alta, Media, Baja
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_entrega_estimada = Column(DateTime(timezone=True), nullable=True)

    # Relaciones (Principio de Integridad)
    # Si borramos un proyecto, sus eventos de bitácora se mantienen o borran según definamos
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

    # Relación inversa: Un contacto pertenece a un proyecto
    proyecto = relationship("Proyecto", back_populates="contactos")

class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    tipo_entrada = Column(String) # Texto, Voz, Email
    contenido = Column(String)
    accion_pendiente = Column(Boolean, default=False)

    # Relación inversa: Una nota pertenece a un proyecto
    proyecto = relationship("Proyecto", back_populates="eventos")