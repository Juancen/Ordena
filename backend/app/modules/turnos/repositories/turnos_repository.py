from app.db.connection import get_connection
from sqlalchemy import text
from app.modules.turnos.models.models_turno import Profesional,Profesional_Servicio


def get_profesional(db, profesional_id):

    query = """
        SELECT id 
        FROM profesionales 
        WHERE id = :profesional_id
    """
    result = db.execute(
        text(query),
        {"profesional_id": profesional_id}
    )
    return result.mappings().first()

def get_servicio(db, servicio_id):

    query = """
        SELECT duracion 
        FROM servicios 
        WHERE id = :servicio_id
    """

    result = db.execute(
        text(query),
        {"servicio_id": servicio_id}
    )

    return result.mappings().first()


def get_agenda(db,profesional_id, dia_semana):

    
    query = """
        SELECT hora_inicio, hora_fin
        FROM agendas
        WHERE profesional_id = :profesional_id 
AND dia_semana = :dia_semana
    """

    
    results =db.execute(
        text(query),
        {
            "profesional_id": profesional_id,
            "dia_semana": dia_semana
        }
    )
    

    return results.mappings().all()


def get_turnos(db,profesional_id, fecha):


    cursor = db.cursor(dictionary=True)

    query = """
        SELECT hora_inicio, hora_fin
        FROM turnos
        WHERE profesional_id = %s
        AND fecha = %s
        AND estado != 'cancelado'
    """

    cursor.execute(query, (profesional_id, fecha))
    results = cursor.fetchall()

    cursor.close()

    return results


def crear_turno(db, turno_data):
    query = """
        INSERT INTO turnos (
            profesional_id,
            servicio_id,
            fecha,
            hora_inicio,
            hora_fin,
            cliente_nombre,
            cliente_telefono,
            estado
        )
        VALUES (
            :profesional_id,
            :servicio_id,
            :fecha,
            :hora_inicio,
            :hora_fin,
            :cliente_nombre,
            :cliente_telefono,
            :estado
        )
    """

    result = db.execute(
        text(query),
        {
            "profesional_id": turno_data["profesional_id"],
            "servicio_id": turno_data["servicio_id"],
            "fecha": turno_data["fecha"],
            "hora_inicio": turno_data["hora_inicio"],
            "hora_fin": turno_data["hora_fin"],
            "cliente_nombre": turno_data["cliente_nombre"],
            "cliente_telefono": turno_data["cliente_telefono"],
            "estado": "confirmado"
        }
    )
    db.commit()

    return result.lastrowid

def get_turno_by_id(db, turno_id: int):
    query = """
        SELECT id, estado,fecha, hora_inicio
        FROM turnos
        WHERE id = %s
    """
    
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (turno_id,))
    
    return cursor.fetchone()

def actualizar_estado_turno(db, turno_id: int, estado: str):
    query = """
        UPDATE turnos
        SET estado = %s
        WHERE id = %s
    """
    
    cursor = db.cursor()
    cursor.execute(query, (estado, turno_id))
    db.commit()
    
def listar_turnos_repository(db, profesional_id=None, fecha=None, estado=None):
    query = "SELECT * FROM turnos"
    condiciones = []
    params = []

    if profesional_id:
        condiciones.append("profesional_id = %s")
        params.append(profesional_id)

    if fecha:
        condiciones.append("fecha = %s")
        params.append(fecha)

    if estado:
        condiciones.append("estado = %s")
        params.append(estado)

    # armamos el WHERE solo si hay filtros
    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()

    return result

def existe_turno_solapado(db, profesional_id, fecha, hora_inicio, hora_fin):

    query = """
        SELECT id 
        FROM turnos
        WHERE profesional_id = :profesional_id
        AND fecha = :fecha
        AND estado != 'cancelado'
        AND (
            hora_inicio < :hora_fin
            AND hora_fin > :hora_inicio
        )
    """

    result = db.execute(
        text(query),
        {
            "profesional_id": profesional_id,
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }
    )

    return result.mappings().first()

def get_profesionales_by_servicio(db, servicio_id):
    return db.query(Profesional)\
        .join(Profesional_Servicio, Profesional.id == Profesional_Servicio.profesional_id)\
        .filter(Profesional_Servicio.servicio_id == servicio_id)\
        .all()