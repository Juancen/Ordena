from sqlalchemy import text
from backend.app.modules.turnos.models.models_turno import (
    Profesional,
    Profesional_Servicio,
    Servicio,
    Agenda,
    Turno
    )


def get_profesional(db, profesional_id):

    return db.query(Profesional).filter(Profesional.id == profesional_id).first()


def get_servicio(db, servicio_id):

    return db.query(Servicio).filter(Servicio.id == servicio_id).first()


def get_agenda(db,profesional_id, dia_semana):

    
    return db.query(Agenda).filter(
        Agenda.profesional_id == profesional_id,
        Agenda.dia_semana == dia_semana
    ).all()


def get_turnos(db,profesional_id=None, fecha=None):
    query = db.query(Turno)
    
    if profesional_id is not None:
        query = query.filter(Turno.profesional_id == profesional_id)
    
    if fecha is not None:
        query = query.filter(Turno.fecha == fecha)
    
    query = query.filter(Turno.estado != "cancelado")
    
    return query.all()


def crear_turno(db, turno_data):
    

    nuevo_turno = Turno(
    profesional_id=turno_data.profesional_id,
    servicio_id=turno_data.servicio_id,
    fecha=turno_data.fecha,
    hora_inicio=turno_data.hora_inicio,
    hora_fin=turno_data.hora_fin,
    cliente_nombre=turno_data.cliente_nombre,
    cliente_telefono=turno_data.cliente_telefono,
    estado="confirmado"
)
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    
    return nuevo_turno.id

def get_turno_by_id(db, turno_id: int):
    
    return db.query(Turno).filter(Turno.id == turno_id).first()

def actualizar_estado_turno(db, turno_id: int, estado: str):
    
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if turno is None:
        return None
    
    turno.estado = estado
    db.commit()
    
def listar_turnos_repository(db, profesional_id=None, fecha=None, estado=None):
    query = db.query(Turno)

    if profesional_id is not None:
        query = query.filter(Turno.profesional_id == profesional_id)

    if fecha is not None:
        query = query.filter(Turno.fecha == fecha)

    if estado is not None:
        query = query.filter(Turno.estado == estado)

    return query.all()

def existe_turno_solapado(db, profesional_id, fecha, hora_inicio, hora_fin):

    return db.query(Turno).filter(
        Turno.profesional_id == profesional_id,
        Turno.fecha == fecha,
        Turno.estado != "cancelado",
        Turno.hora_inicio < hora_fin,
        Turno.hora_fin > hora_inicio
    ).first()

def get_profesionales_by_servicio(db, servicio_id):
    return db.query(Profesional)\
        .join(Profesional_Servicio, Profesional.id == Profesional_Servicio.profesional_id)\
        .filter(Profesional_Servicio.servicio_id == servicio_id)\
        .all()