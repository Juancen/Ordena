from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from app.db.database import Base
from sqlalchemy import UniqueConstraint

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
    
class Profesional(Base):
    __tablename__ = "profesionales"
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"))

class Servicio(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    duracion = Column(Integer, nullable=False)
    negocio_id = Column(Integer, ForeignKey("negocios.id"))

class Profesional_Servicio(Base):
    __tablename__ = "profesional_servicio"
    id = Column(Integer, primary_key=True, index=True)
    profesional_id = Column(Integer, ForeignKey("profesionales.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    __table_args__ = (
    UniqueConstraint('profesional_id', 'servicio_id', name='uix_prof_serv'),
)

class Agenda(Base):
    __tablename__ = "agendas"
    id = Column(Integer, primary_key=True, index=True)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    profesional_id = Column(Integer, ForeignKey("profesionales.id"),nullable=False)
    