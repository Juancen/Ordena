from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from backend.app.db.database import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

class TurnoCreate:
    def __init__(self, profesional_id, servicio_id, fecha, hora_inicio, hora_fin, cliente_nombre, cliente_telefono):
        self.profesional_id = profesional_id
        self.servicio_id = servicio_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.cliente_nombre = cliente_nombre
        self.cliente_telefono = cliente_telefono

class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    estado = Column(String(20), default="pendiente")

    cliente_nombre = Column(String(100))
    cliente_telefono = Column(String(20))

    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    profesional_id = Column(Integer, ForeignKey("profesionales.id"))
    
    profesional = relationship("Profesional", back_populates="turnos")
    servicio = relationship("Servicio", back_populates="turnos")
    
class Profesional(Base):
    __tablename__ = "profesionales"
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"))
    agendas = relationship("Agenda", back_populates="profesional")
    turnos = relationship("Turno", back_populates="profesional")
    profesional_servicio = relationship("Profesional_Servicio", back_populates="profesional")

class Servicio(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    duracion = Column(Integer, nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"))
    precio = Column(Integer, nullable=False)
    turnos = relationship("Turno", back_populates="servicio")
    profesional_servicio = relationship("Profesional_Servicio", back_populates="servicio")

class Profesional_Servicio(Base):
    __tablename__ = "profesional_servicio"
    id = Column(Integer, primary_key=True, index=True)
    profesional_id = Column(Integer, ForeignKey("profesionales.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    __table_args__ = (
    UniqueConstraint('profesional_id', 'servicio_id', name='uix_prof_serv')),
    profesional = relationship("Profesional", back_populates="profesional_servicio")
    servicio = relationship("Servicio", back_populates="profesional_servicio")


class Agenda(Base):
    __tablename__ = "agendas"
    id = Column(Integer, primary_key=True, index=True)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    profesional_id = Column(Integer, ForeignKey("profesionales.id"),nullable=False)
    profesional = relationship("Profesional", back_populates="agendas")
    