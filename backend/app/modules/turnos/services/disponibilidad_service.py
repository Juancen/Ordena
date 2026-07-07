from datetime import datetime
from backend.app.modules.turnos.models.models_turno import Turno
from fastapi import HTTPException
from backend.app.modules.turnos.services.calculos import (
    filtrar_pasado,
    calcular_slots
)
from backend.app.modules.turnos.repositories.turnos_repository import (
    get_servicio,
    get_agenda,
    get_turnos,
    get_profesionales_by_servicio
)
def get_agenda_completa(db_orm,profesional_id, dia_semana, fecha,servicio_id):
    hoy = datetime.now().date()
    agendas = get_agenda(db_orm,profesional_id, dia_semana)
    
    if not agendas:
        return []
    
    # traer turnos (ORM)
    turnos = db_orm.query(Turno)\
    .filter(Turno.profesional_id == profesional_id)\
    .filter(Turno.fecha == fecha)\
    .filter(Turno.estado != "cancelado")\
    .all()
    
    #  convertirlos
    turnos_convertidos = convertir_turnos(turnos, fecha)

    # ordenar turnos
    turnos = sorted(turnos_convertidos, key=lambda t: t["hora_inicio"])
    
    # servicio (duración)
    servicio = get_servicio(db_orm,servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="El servicio no existe")
    
    duracion = servicio.duracion
    
    # 5. armar bloques agenda (datetime)
    bloques_agendas = construir_bloques_agenda(agendas,fecha)
    
    
    resultado_slots = calcular_slots(bloques_agendas,turnos,duracion)
    
    
    # 7. filtrar pasado
    slots = filtrar_pasado(resultado_slots, fecha)
    
        
    if fecha == hoy and not slots:
            raise HTTPException(status_code=409, detail="El horario no está disponible")
    
    return slots

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
    
    turnos_convertidos = convertir_turnos(turnos,fecha) 

    # ordenar turnos
    turnos = sorted(turnos_convertidos, key=lambda t: t["hora_inicio"])

    # 5. armar bloques agenda (datetime)
    bloques_agendas = construir_bloques_agenda(agendas,fecha)
    
    resultado_slots = calcular_slots(bloques_agendas,turnos,duracion)
    

    # 7. filtrar pasado
    slots = filtrar_pasado(resultado_slots, fecha)
    
    if fecha == hoy and not slots:
        raise HTTPException(status_code=409, detail="El horario no está disponible")

    return slots

def construir_bloques_agenda(agendas, fecha):
    bloques_agenda = []

    for a in agendas:
        
        inicio = datetime.combine(fecha, a.hora_inicio)
        fin = datetime.combine(fecha, a.hora_fin)
        
        bloques_agenda.append((inicio, fin))
    
    return bloques_agenda

def convertir_turnos(turnos, fecha):
    turnos_convertidos = []

    for t in turnos:
        inicio = datetime.combine(fecha, t.hora_inicio)
        fin = datetime.combine(fecha, t.hora_fin)

        turnos_convertidos.append({
            "hora_inicio": inicio,
            "hora_fin": fin
        })
    
    return turnos_convertidos

def listar_profesionales_por_servicio(db, servicio_id):
    profesionales = get_profesionales_by_servicio(db, servicio_id)

    return [
        {
            "id": p.id,
            "nombre": p.nombre
        }
        for p in profesionales
    ]