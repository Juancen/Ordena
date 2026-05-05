from app.modules.turnos.services.disponibilidad_service import get_disponibilidad
from app.modules.turnos.services.turno_service import crear_turno_service
from app.modules.turnos.schemas.turno import CrearTurnoRequest
from app.db.dependencies import get_db
from fastapi import Depends
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()

@router.get("/disponibilidad")
def disponibilidad(profesional_id: int, servicio_id: int, fecha: str, db=Depends(get_db)):

    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()

    slots = get_disponibilidad(profesional_id, servicio_id, fecha_dt,db)

    return [
        {
            "inicio": s[0].strftime("%H:%M"),
            "fin": s[1].strftime("%H:%M")
        }
        for s in slots
    ]

@router.post("/turnos")
def crear_turno_endpoint(data: CrearTurnoRequest, db=Depends(get_db)):
    
    print("DB en endpoint:", db)
    turno_id = crear_turno_service(db, data)
    

    return {
        "message": "Turno creado correctamente",
        "turno_id": turno_id
    }