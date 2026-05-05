from app.db.connection import get_connection

def get_servicio(db, servicio_id):
    
    cursor = db.cursor(dictionary=True)

    query = "SELECT duracion FROM servicio WHERE id = %s"
    cursor.execute(query, (servicio_id,))

    result = cursor.fetchone()

    cursor.close()  # ✔️ esto sí
    
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