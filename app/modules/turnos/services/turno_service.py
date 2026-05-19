from datetime import datetime, timedelta
from fastapi import HTTPException
from app.modules.turnos.repositories.turnos_repository import (
    crear_turno,
    get_servicio,
    get_turno_by_id,
    get_profesional,
    actualizar_estado_turno,
    listar_turnos_repository,
    existe_turno_solapado,
    get_agenda
    )

def crear_turno_service(db, data):
    
    hoy = datetime.now().date()
    ahora = datetime.now()
    
    

    # 1. Datos del request (strings)
    profesional_id = data.profesional_id
    servicio_id = data.servicio_id
    fecha_str = data.fecha
    hora_inicio_str = data.hora_inicio

    # 2. Convertir a datetime (para lógica)
    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    hora_inicio_dt = datetime.strptime(hora_inicio_str, "%H:%M")
    hora_inicio_dt = datetime.combine(fecha_dt, hora_inicio_dt.time())
    
    if fecha_dt < hoy:
        raise HTTPException(
        status_code=400,
        detail="No se puede crear turnos en fechas pasadas"
    )
        
    if fecha_dt == hoy and hora_inicio_dt <= ahora:
        raise HTTPException(
        status_code=400,
        detail="No se puede crear turnos en horarios pasados"
    )
        
    # profesional 
    profesional = get_profesional(db, profesional_id)
    if not profesional:
        raise HTTPException(status_code=404, detail="El profesional no existe")
    
    # agenda
    dia_semana = fecha_dt.weekday() + 1
    agendas = get_agenda(db, profesional_id, dia_semana)
    print("AGENDAS:", agendas)
    print("DIA SEMANA:", dia_semana)

    if not agendas:
        raise HTTPException(
    status_code=400,
    detail="El profesional no trabaja ese día"
)

    # 3. Obtener duración
    servicio = get_servicio(db, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404,detail="Servicio no existe")
    duracion = servicio["duracion"]

    # 4. Calcular hora fin
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion)
    
    # 7. Convertir a string para guardar
    hora_inicio_db = hora_inicio_dt.strftime("%H:%M")
    hora_fin_db = hora_fin_dt.strftime("%H:%M")

    # validar que el horario esté dentro de algún bloque
    dentro_agenda = False

    for a in agendas:
        inicio = (datetime.min + a["hora_inicio"]).time()
        fin = (datetime.min + a["hora_fin"]).time()

        if inicio <= hora_inicio_dt.time() and hora_fin_dt.time() <= fin:
            dentro_agenda = True
            break

    if not dentro_agenda:
        raise HTTPException(400, "El horario está fuera de la agenda")
    
    # validar solapamiento
    conflicto = existe_turno_solapado(
    db,
    profesional_id,
    fecha_str,
    hora_inicio_db,
    hora_fin_db
)

    if conflicto:
        raise HTTPException(
        status_code=409,
        detail="El horario ya está ocupado"
    )

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

def cancelar_turno_service(db, turno_id: int):
    hoy = datetime.now().date()
    ahora = datetime.now()
    
    # 1. Buscar turno
    turno = get_turno_by_id(db, turno_id)
    
    if not turno:
        raise HTTPException(status_code=404, detail="El turno no existe")
    
    # 2. Validar estado
    if turno["estado"] == "cancelado":
       raise HTTPException(status_code=400, detail="El turno ya está cancelado")
   
    if turno["fecha"] < hoy:
        raise HTTPException(400, "No se puede cancelar un turno pasado")
    
    hora = turno["hora_inicio"]
    if isinstance(hora, timedelta):
        hora = (datetime.min + hora).time()

    inicio_turno = datetime.combine(turno["fecha"], hora)
    
    # 🔥 REGLA DE NEGOCIO
    if inicio_turno - ahora < timedelta(hours=48):
        raise HTTPException(
    status_code=400,
    detail="No se puede cancelar con menos de 48 hs de anticipación"
)
    
    # 3. Cancelar
    actualizar_estado_turno(db, turno_id, "cancelado")
    
    return {"message": "Turno cancelado correctamente"}

def listar_turnos_service(db, profesional_id=None, fecha=None, estado=None):

    if estado and estado not in ["confirmado", "cancelado"]:
        raise HTTPException(400, "Estado inválido")

    turnos = listar_turnos_repository(
        db,
        profesional_id=profesional_id,
        fecha=fecha,
        estado=estado
    )
    if not turnos:
        return []

    return turnos