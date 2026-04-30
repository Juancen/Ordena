from datetime import datetime

from app.modules.turnos.services.calculos import (
    calcular_bloques_libres,
    generar_slots,
    filtrar_pasado
)
from app.modules.turnos.repositories.turnos_repository import (
    get_servicio,
    get_agenda,
    get_turnos
)
def get_disponibilidad(profesional_id, servicio_id, fecha):

    # 1. servicio (duración)
    servicio = get_servicio(servicio_id)
    if not servicio:
        return []
    duracion = servicio["duracion"]

    # 2. día de la semana
    dia_semana = fecha.weekday() + 1  # ajustalo si usás otro formato

    # 3. agenda
    agendas = get_agenda(profesional_id, dia_semana)

    if not agendas:
        return []

    # 4. turnos ocupados
    turnos = get_turnos(profesional_id, fecha)
    
    turnos_convertidos = []

    for t in turnos:
        hora_inicio = (datetime.min + t["hora_inicio"]).time()
        hora_fin = (datetime.min + t["hora_fin"]).time()

        inicio = datetime.combine(fecha, hora_inicio)
        fin = datetime.combine(fecha, hora_fin)

        turnos_convertidos.append({
            "hora_inicio": inicio,
            "hora_fin": fin
        })

    turnos = turnos_convertidos

    # ordenar turnos
    turnos = sorted(turnos, key=lambda t: t["hora_inicio"])

    # 5. armar bloques agenda (datetime)
    bloques_agenda = []

    for a in agendas:
        
        hora_inicio = (datetime.min + a["hora_inicio"]).time()
        hora_fin = (datetime.min + a["hora_fin"]).time()
        
        inicio = datetime.combine(fecha, hora_inicio)
        fin = datetime.combine(fecha, hora_fin)
        
        bloques_agenda.append((inicio, fin))

    # 6. calcular bloques libres
    bloques_libres = calcular_bloques_libres(bloques_agenda, turnos)

    # 7. generar slots
    slots = generar_slots(bloques_libres, duracion)

    # 8. filtrar pasado
    slots = filtrar_pasado(slots, fecha)

    return slots