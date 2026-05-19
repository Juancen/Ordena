from datetime import datetime
from fastapi import HTTPException
from app.modules.turnos.services.calculos import (
    calcular_bloques_libres,
    generar_slots,
    filtrar_pasado
)
from app.modules.turnos.repositories.turnos_repository import (
    get_servicio,
    get_agenda,
    get_turnos,
)


def get_disponibilidad(db,profesional_id, servicio_id, fecha):
    
    hoy = datetime.now().date()
    
    if fecha < hoy:
        raise HTTPException(
        status_code=400,
        detail="No se puede consultar disponibilidad de fechas pasadas"
    )
    

    # servicio (duración)
    servicio = get_servicio(db,servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="El servicio no existe")
    
    duracion = servicio["duracion"]

    #. día de la semana
    dia_semana = fecha.weekday() + 1

    #  agenda
    agendas = get_agenda(db,profesional_id, dia_semana)
    if not agendas:
        return []

    #  turnos ocupados
    turnos = get_turnos(db,profesional_id, fecha)
    
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
    
    if fecha == hoy and not slots:
        raise HTTPException(status_code=409, detail="El horario no está disponible")

    return slots