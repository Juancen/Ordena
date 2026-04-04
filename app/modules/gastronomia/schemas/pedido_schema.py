from pydantic import BaseModel

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