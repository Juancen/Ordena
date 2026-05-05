from pydantic import BaseModel

class TurnoCreate(BaseModel):
    fecha: str
    hora_inicio: str
    servicio_id: int
    profesional_id: int

class CrearTurnoRequest(BaseModel):
    profesional_id: int
    servicio_id: int
    fecha: str
    hora_inicio: str
    cliente_nombre: str
    cliente_telefono: str