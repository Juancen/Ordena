from datetime import timedelta
from datetime import datetime

def calcular_bloques_libres(bloques_agenda, turnos):
    bloques_libres = []

    for bloque_inicio, bloque_fin in bloques_agenda:
        actual_inicio = bloque_inicio

        for turno in turnos:
            turno_inicio = turno["hora_inicio"]
            turno_fin = turno["hora_fin"]

            # ignorar turnos fuera del bloque
            if turno_fin <= actual_inicio or turno_inicio >= bloque_fin:
                continue

            # si hay espacio antes del turno
            if actual_inicio < turno_inicio:
                bloques_libres.append((actual_inicio, turno_inicio))

            # mover el inicio al final del turno
            actual_inicio = max(actual_inicio, turno_fin)

        # si queda espacio al final del bloque
        if actual_inicio < bloque_fin:
            bloques_libres.append((actual_inicio, bloque_fin))

    return bloques_libres



def generar_slots(bloques_libres, duracion_minutos):
    slots = []

    for inicio, fin in bloques_libres:
        actual = inicio

        while actual + timedelta(minutes=duracion_minutos) <= fin:
            slot_fin = actual + timedelta(minutes=duracion_minutos)

            slots.append((actual, slot_fin))

            actual = slot_fin

    return slots

def filtrar_pasado(slots, fecha):
    ahora = datetime.now()

    resultado = []

    for slot in slots:
        inicio = slot["inicio"]

        if fecha == ahora.date():
            if inicio <= ahora:
                continue

        resultado.append(slot) 

    return resultado

def calcular_slots(bloques_agenda,turnos,duracion):
    
    slots = generar_slots(bloques_agenda, duracion)
    
    resultado = []
    
    for  s_inicio, s_fin in slots:
    
        ocupado = any( s_inicio < t["hora_fin"] and s_fin > t["hora_inicio"]
            for t in turnos
    )
    
        resultado.append({
            "inicio": s_inicio,
            "fin": s_fin,
            "estado": "ocupado" if ocupado else "disponible"
            })
        
    resultado = sorted(resultado, key=lambda x: x["inicio"])
    
    return resultado
    
