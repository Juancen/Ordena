from app.db.connection import get_connection

def get_servicio(servicio_id):
    conn = get_connection()
    
    if conn is None:
        raise Exception("Error: no se pudo conectar a la base de datos")
    
    cursor = conn.cursor(dictionary=True)
    query = "SELECT duracion FROM servicio WHERE id = %s"
    cursor.execute(query, (servicio_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def get_agenda(profesional_id, dia_semana):
    conn = get_connection()
    
    if conn is None:
        raise Exception("Error: no se pudo conectar a la base de datos")

    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT hora_inicio, hora_fin
        FROM agenda
        WHERE profesional_id = %s AND dia_semana = %s
    """

    cursor.execute(query, (profesional_id, dia_semana))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


def get_turnos(profesional_id, fecha):
    conn = get_connection()
    
    if conn is None:
        raise Exception("Error: no se pudo conectar a la base de datos")

    cursor = conn.cursor(dictionary=True)

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
    conn.close()

    return results