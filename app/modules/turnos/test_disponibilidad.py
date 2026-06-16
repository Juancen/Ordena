from datetime import datetime
from app.modules.turnos.services.turnos_service import calcular_bloques_libres
from app.modules.turnos.services.turnos_service import generar_slots

bloques_agenda = [
    (datetime(2026, 5, 4, 10, 0), datetime(2026, 5, 4, 13, 0))
]

turnos = [
    {"hora_inicio": datetime(2026, 5, 4, 10, 30), "hora_fin": datetime(2026, 5, 4, 11, 0)},
    {"hora_inicio": datetime(2026, 5, 4, 11, 30), "hora_fin": datetime(2026, 5, 4, 12, 0)},
]

duracion = 30
bloques_libres = calcular_bloques_libres(bloques_agenda, turnos)

print("BLOQUES LIBRES:")
for b in bloques_libres:
    print(b)

slots = generar_slots(bloques_libres, duracion)

print("\nSLOTS:")
for s in slots:
    print(s)