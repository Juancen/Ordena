from app.db.connection import get_connection

def get_profesional(db, profesional_id):
    cursor = db.cursor(dictionary=True)

    query = "SELECT id FROM profesional WHERE id = %s"
    cursor.execute(query, (profesional_id,))

    result = cursor.fetchone()

    cursor.close()

    return result

def get_servicio(db, servicio_id):
    
    cursor = db.cursor(dictionary=True)

    query = "SELECT duracion FROM servicio WHERE id = %s"
    cursor.execute(query, (servicio_id,))

    result = cursor.fetchone()

    cursor.close()
    
    return result


def get_agenda(db,profesional_id, dia_semana):

    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT hora_inicio, hora_fin
        FROM agenda
        WHERE profesional_id = %s AND dia_semana = %s
    """

    cursor.execute(query, (profesional_id, dia_semana))
    results = cursor.fetchall()

    cursor.close()

    return results


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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        turno_data["profesional_id"],
        turno_data["servicio_id"],
        turno_data["fecha"],
        turno_data["hora_inicio"],
        turno_data["hora_fin"],
        turno_data["cliente_nombre"],
        turno_data["cliente_telefono"],
        "confirmado"
    )

    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()

    return cursor.lastrowid

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
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT id FROM turnos
        WHERE profesional_id = %s
        AND fecha = %s
        AND estado != 'cancelado'
        AND (
            hora_inicio < %s
            AND hora_fin > %s
        )
    """

    cursor.execute(query, (profesional_id, fecha, hora_fin, hora_inicio))

    result = cursor.fetchone()

    cursor.close()

    return result