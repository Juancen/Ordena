from app.modules.turnos.services.disponibilidad_service import get_disponibilidad
from app.modules.turnos.services.turno_service import (
    crear_turno_service,
    cancelar_turno_service,
    listar_turnos_service
    )
from app.modules.turnos.schemas.turno import CrearTurnoRequest
from app.db.dependencies import get_db
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
router = APIRouter()
from typing import Optional

@router.get("/disponibilidad")
def disponibilidad(profesional_id: int, servicio_id: int, fecha: str, db=Depends(get_db)):

    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    slots = get_disponibilidad(db,profesional_id, servicio_id, fecha_dt)

    return [
        {
            "inicio": s[0].strftime("%H:%M"),
            "fin": s[1].strftime("%H:%M")
        }
        for s in slots
    ]

@router.post("/turnos")
def crear_turno_endpoint(data: CrearTurnoRequest, db=Depends(get_db)):
    
        turno_id = crear_turno_service(db, data)
        
        return {
        "message": "Turno creado correctamente",
        "turno_id": turno_id
        }

@router.patch("/turnos/{turno_id}/cancelar")
def cancelar_turno(turno_id: int, db: Session = Depends(get_db)):
    try:
        return cancelar_turno_service(db, turno_id)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/turnos")
def listar_turnos(
    profesional_id: Optional[int] = None,
    fecha: Optional[date] = None,
    estado: Optional[str] = None,
    db = Depends(get_db)
):
    try:
        turnos = listar_turnos_service(
            db,
            profesional_id=profesional_id,
            fecha=fecha,
            estado=estado
        )
        return turnos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))