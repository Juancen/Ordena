from pydantic import BaseModel
from decimal import Decimal

class ProductoCreate(BaseModel):
    id_negocio: int
    nombre: str
    precio: float
    


class ProductoResponse(BaseModel):
    id: int
    id_negocio: int
    nombre: str
    precio: Decimal
    estado: str

class ProductoEstadoUpdate(BaseModel):
    estado: str

class ProductoUpdate(BaseModel):
    nombre: str
    precio: float

class MensajeResponse(BaseModel):
    message: str