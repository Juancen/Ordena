from app.modules.turnos.services.disponibilidad_service import get_disponibilidad
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()

@router.get("/disponibilidad")
def disponibilidad(profesional_id: int, servicio_id: int, fecha: str):

    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()

    slots = get_disponibilidad(profesional_id, servicio_id, fecha_dt)

    return [
        {
            "inicio": s[0].strftime("%H:%M"),
            "fin": s[1].strftime("%H:%M")
        }
        for s in slots
    ]