from backend.app.modules.turnos.services.disponibilidad_service import (
    get_disponibilidad,
    get_agenda_completa,
    listar_profesionales_por_servicio)
from backend.app.modules.turnos.services.turno_service import (
    crear_turno_service,
    cancelar_turno_service,
    listar_turnos_service
    )
from backend.app.modules.turnos.models.models_turno import Servicio
from backend.app.db.database import SessionLocal
from backend.app.modules.turnos.models.models_turno import Turno
from backend.app.modules.turnos.schemas.turno import CrearTurnoRequest
from backend.app.db.dependencies import get_db,get_db_orm
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
router = APIRouter()
from typing import Optional

@router.get("/profesionales")
def get_profesionales(servicio_id: int, db: Session = Depends(get_db_orm)):
    return listar_profesionales_por_servicio(db, servicio_id)


@router.get("/agenda-completa")
def agenda_completa(profesional_id: int, servicio_id: int, fecha: str, db=Depends(get_db_orm)):

    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()

    dia_semana = fecha_dt.weekday() + 1

    agenda = get_agenda_completa(
        db,
        profesional_id,
        dia_semana,
        fecha_dt,
        servicio_id
    )
    return [
        {
        "inicio": a["inicio"].strftime("%H:%M"),
        "fin": a["fin"].strftime("%H:%M"),
        "estado": a["estado"]
        }
        for a in agenda
    ]

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
def crear_turno_endpoint(data: CrearTurnoRequest, db: Session=Depends(get_db_orm)):
    
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
    db = Depends(get_db_orm)
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

@router.get("/servicios")
def get_servicios(db: Session = Depends(get_db_orm)):
    return db.query(Servicio).all()