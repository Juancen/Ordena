from pydantic import BaseModel

class TurnoCreate(BaseModel):
    fecha: str
    hora_inicio: str
    servicio_id: int
    profesional_id: int