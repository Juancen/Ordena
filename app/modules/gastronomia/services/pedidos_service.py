from app.modules.gastronomia.exceptions.pedidos_errors import NotFoundError
from app.modules.gastronomia.exceptions.pedidos_errors import ProductoNoPerteneceAlNegocioError
from app.modules.gastronomia.exceptions.pedidos_errors import ValidationError
from app.modules.gastronomia.exceptions.pedidos_errors import PedidoInvalidError
from app.modules.gastronomia.repositories.pedidos_repository import obtener_productos_por_ids

def validar_items_pedido(items_pedido):
    
    if not items_pedido or not isinstance(items_pedido, list):
        raise ValueError("items_pedido debe ser una lista no vacía")

    for index, item in enumerate(items_pedido):
        
        if not isinstance(item, dict):
            raise ValueError(f"Item en posición {index} no es válido")
        if "id_producto" not in item:
            raise ValueError(f"Item en posición {index} sin id_producto")
        if "cantidad" not in item:
            raise ValueError(f"Item en posición {index} sin cantidad")
        
        id_producto = item["id_producto"]
        cantidad = item["cantidad"]
        
        if not isinstance(id_producto, int):
            raise ValueError(f"id_producto inválido en posición {index}")

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError(f"cantidad inválida en posición {index}")
        
def crear_pedido(id_negocio,nombre_cliente,contacto_cliente,direccion_cliente,tipo_entrega,origen,items_pedido):
    
    TIPO_ENTREGAS = ["delivery", "retiro_local"]
    TIPO_ORIGEN = ["interno","online"]
    
    if not id_negocio:
        raise NotFoundError("Negocio con id indicado no se encontro")
    if not nombre_cliente:
        raise ValidationError("nombre del cliente invalido")
    if not contacto_cliente:
        raise ValidationError("contacto del cliente invalido")
    if tipo_entrega not in TIPO_ENTREGAS:
        raise PedidoInvalidError("tipo de entrega invalido")
    if tipo_entrega == TIPO_ENTREGAS[0]:
        if not direccion_cliente:
            raise PedidoInvalidError("direccion de cliente obligatoria")
    if origen not in TIPO_ORIGEN:
        raise NotFoundError("tipo de origen invalido")
    
    validar_items_pedido(items_pedido)
    
    
    
    ids_productos = [item["id_producto"] for item in items_pedido]
    productos_db = obtener_productos_por_ids(ids_productos)
    ids_encontrados = [p["id"] for p in productos_db or []] # type: ignore
    faltantes = set(ids_productos) - set(ids_encontrados)
    
    if faltantes:
        raise ValueError(f"Faltan productos: {faltantes}")
    
    for producto in productos_db:
        if producto["id_negocio"] != id_negocio: # type: ignore
            raise ProductoNoPerteneceAlNegocioError("id del producto no coincide con id negocio")
    