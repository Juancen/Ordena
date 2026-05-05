from datetime import datetime, timedelta

from app.modules.turnos.repositories.turnos_repository import (crear_turno,get_servicio)
from app.modules.turnos.services.disponibilidad_service import get_disponibilidad

def crear_turno_service(db, data):

    # 1. Datos del request (strings)
    profesional_id = data.profesional_id
    servicio_id = data.servicio_id
    fecha_str = data.fecha
    hora_inicio_str = data.hora_inicio

    # 2. Convertir a datetime (para lógica)
    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")

    hora_inicio_dt = datetime.strptime(hora_inicio_str, "%H:%M")
    hora_inicio_dt = datetime.combine(fecha_dt, hora_inicio_dt.time())

    # 3. Obtener duración
    servicio = get_servicio(db, servicio_id)
    if not servicio:
        raise Exception("Servicio no existe")

    duracion = servicio["duracion"]

    # 4. Calcular hora fin
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion)

    # 5. Obtener disponibilidad
    disponibilidad = get_disponibilidad(
        db,
        profesional_id,
        servicio_id,
        fecha_dt
    )

    # 6. Validar slot
    slot_valido = False

    for slot in disponibilidad:
        if slot[0] == hora_inicio_dt:
            slot_valido = True
            break

    if not slot_valido:
        raise Exception("El horario no está disponible")

    # 7. Convertir a string para guardar
    hora_inicio_db = hora_inicio_dt.strftime("%H:%M")
    hora_fin_db = hora_fin_dt.strftime("%H:%M")

    # 8. Crear turno
    turno_data = {
    "profesional_id": profesional_id,
    "servicio_id": servicio_id,
    "fecha": fecha_str,
    "hora_inicio": hora_inicio_db,
    "hora_fin": hora_fin_db,
    "cliente_nombre": data.cliente_nombre,
    "cliente_telefono": data.cliente_telefono
}

    turno_id = crear_turno(db, turno_data)

    return turno_id