from pydantic import BaseModel
from datetime import datetime

class ItemPedidoCreate(BaseModel):
    id_producto: int
    cantidad: int

class PedidoCreate(BaseModel):
    id_negocio: int
    nombre_cliente: str
    contacto_cliente: str
    direccion_cliente: str | None = None
    tipo_entrega: str
    origen: str
    items_pedido: list[ItemPedidoCreate]

class PedidoResponse(BaseModel):
    id: int
    codigo_publico: str
    nombre_cliente: str
    contacto_cliente: str
    direccion_cliente: str | None
    tipo_entrega: str
    origen: str
    estado: str
    precio_total: float

class ActualizarEstadoPedido(BaseModel):
    estado: str

class PedidoEstadoResponse(BaseModel):
    id: int
    codigo_publico: str
    estado: str

class PedidoListItem(BaseModel):
    codigo_publico: str
    nombre_cliente: str
    tipo_entrega: str
    estado: str
    fecha_creacion: datetime
    precio_total: float

class ItemPedidoResponse(BaseModel):
    id_producto: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class PedidoDetalleResponse(BaseModel):
    id: int
    codigo_publico: str
    nombre_cliente: str
    contacto_cliente: str
    direccion_cliente: str | None
    tipo_entrega: str
    origen: str
    estado: str
    precio_total: float
    fecha_creacion: datetime
    items: list[ItemPedidoResponse]

class PaginacionResponse(BaseModel):
    total:float
    limit:int
    offset:int
    has_next:int
    items:list