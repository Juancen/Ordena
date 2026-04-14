from app.modules.gastronomia.exceptions.pedidos_errors import ProductoNoPerteneceAlNegocioError
from app.modules.gastronomia.exceptions.pedidos_errors import (
    ValidationError,
    PedidoInvalidError,
    ProductosNoEncontradosError,
    NegocioNoEncontradoError,
    PedidoNoEncontradoError,
)
from app.modules.gastronomia.repositories.negocio_repository import obtener_negocio_por_id
from app.modules.gastronomia.repositories.producto_repository import obtener_productos_por_ids
from app.modules.gastronomia.repositories.pedidos_repository import (
    obtener_pedido_por_codigo_publico,
    crear_pedido_con_items,
    obtener_pedido_por_id,
    repository_actualizar_estado_pedido,
    obtener_pedidos,
    obtener_items_por_pedido,
    contar_pedidos
    )
import random
import string
ESTADOS_PEDIDO_VALIDOS = ["pendiente", "en_preparacion", "listo", "entregado", "cancelado"]
MAX_LIMIT = 50
from datetime import timedelta
from datetime import datetime
def generar_codigo_publico(longitud=4):
    letras_upper = string.ascii_uppercase 
    numeros = string.digits
    codigo_letras = ''.join(random.choices(letras_upper, k=longitud))
    codigo_numeros = ''.join(random.choices(numeros, k=longitud))
    return f"{codigo_letras}-{codigo_numeros}"

def crear_codigo_publico_unico():
    while True:
        codigo = generar_codigo_publico()
        existente = obtener_pedido_por_codigo_publico(codigo)

        if not existente:
            return codigo
def validar_items_duplicados(items):
    ids_vistos = set()

    for item in items:
        id_producto = item["id_producto"]

        if id_producto in ids_vistos:
            raise ValidationError(f"Producto duplicado: {id_producto}")

        ids_vistos.add(id_producto)
def validar_items_pedido(items_pedido):
    
    if not items_pedido or not isinstance(items_pedido, list):
        raise ValidationError("items_pedido debe ser una lista no vacía")

    for index, item in enumerate(items_pedido):
        
        if not isinstance(item, dict):
            raise ValidationError(f"Item en posición {index} no es válido")
        if "id_producto" not in item:
            raise ValidationError(f"Item en posición {index} sin id_producto")
        if "cantidad" not in item:
            raise ValidationError(f"Item en posición {index} sin cantidad")
        
        id_producto = item["id_producto"]
        cantidad = item["cantidad"]
        
        if not isinstance(id_producto, int):
            raise ValidationError(f"id_producto inválido en posición {index}")

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidationError(f"cantidad inválida en posición {index}")
        
def crear_pedido(id_negocio,nombre_cliente,contacto_cliente,direccion_cliente,tipo_entrega,origen,items_pedido):
    
    TIPO_ENTREGAS = ["delivery", "retiro_local"]
    TIPO_ORIGEN = ["interno","online"]
    
    nombre_cliente = nombre_cliente.strip().lower() if nombre_cliente else nombre_cliente
    contacto_cliente = contacto_cliente.strip() if contacto_cliente else contacto_cliente
    direccion_cliente = direccion_cliente.strip() if direccion_cliente else direccion_cliente
    
    if not id_negocio:
        raise ValidationError("id_negocio es obligatorio")
    if not nombre_cliente:
        raise ValidationError("nombre del cliente invalido")
    if not contacto_cliente:
        raise ValidationError("contacto del cliente invalido")
    if tipo_entrega not in TIPO_ENTREGAS:
        raise PedidoInvalidError("tipo de entrega invalido")
    if tipo_entrega == "delivery":
        if not direccion_cliente:
            raise PedidoInvalidError("direccion de cliente obligatoria")
        elif tipo_entrega == "retiro_local":
            direccion_cliente = None
    if origen not in TIPO_ORIGEN:
        raise ValidationError("origen invalido")
    
    negocio = obtener_negocio_por_id(id_negocio)
    if not negocio:
        raise NegocioNoEncontradoError(f"Negocio {id_negocio} no existe")
    
    validar_items_pedido(items_pedido)
    validar_items_duplicados(items_pedido)
    
    ids_productos = [item["id_producto"] for item in items_pedido]
    productos_db = obtener_productos_por_ids(ids_productos)
    ids_encontrados = [p["id"] for p in productos_db] # type: ignore
    faltantes = set(ids_productos) - set(ids_encontrados)
    
    if faltantes:
        raise ProductosNoEncontradosError(list(faltantes))
    
    for producto in productos_db:
        if producto["id_negocio"] != id_negocio: # type: ignore
            raise ProductoNoPerteneceAlNegocioError("Uno o más productos no pertenecen al negocio indicado")
    
    productos_por_id = {producto["id"]: producto for producto in productos_db} # type: ignore

    items_preparados = []
    precio_total = 0

    for item in items_pedido:
        
        id_producto = item["id_producto"]
        cantidad = item["cantidad"]
        producto = productos_por_id[id_producto]
        precio_unitario = producto["precio"] # type: ignore
        subtotal = cantidad * precio_unitario
        precio_total += subtotal

        items_preparados.append({
            
        "id_producto": id_producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario
        
    })

    
    codigo_publico = crear_codigo_publico_unico()
    estado = "pendiente"
    pedido_creado = crear_pedido_con_items(
        id_negocio=id_negocio,
        nombre_cliente=nombre_cliente,
        contacto_cliente=contacto_cliente,
        direccion_cliente=direccion_cliente,
        tipo_entrega=tipo_entrega,
        origen=origen,
        estado=estado,
        precio_total=precio_total,
        codigo_publico=codigo_publico,
        items=items_preparados
)

    return pedido_creado

def consultar_pedido_por_codigo_publico(codigo_publico):

    # 1. validar que venga algo
    if not codigo_publico:
        raise ValidationError("codigo_publico es obligatorio")

    # 2. limpiar
    codigo_publico = codigo_publico.strip()

    if not codigo_publico:
        raise ValidationError("codigo_publico invalido")

    # 3. buscar en DB
    pedido = obtener_pedido_por_codigo_publico(codigo_publico)

    # 4. validar existencia
    if not pedido:
        raise PedidoNoEncontradoError(f"No existe pedido con codigo {codigo_publico}")

    # 5. devolver
    return pedido

def actualizar_estado_pedido(id_pedido, nuevo_estado):
    
    if not id_pedido:
        raise ValidationError("id del pedido es obligatorio")
    
    nuevo_estado = nuevo_estado.strip() if nuevo_estado else nuevo_estado
    
    if not nuevo_estado:
        raise ValidationError("Estado del pedido es obligatorio")
    
    if nuevo_estado not in ESTADOS_PEDIDO_VALIDOS:
        raise ValidationError("Estado del pedido es invalido")
    
    pedido = obtener_pedido_por_id(id_pedido)
    
    if not pedido:
        raise PedidoNoEncontradoError("El pedido con el ID indicado no existe")
    
    estado_actual = pedido["estado"]
    print(repr(estado_actual))
    
    validar_transicion_estado(estado_actual, nuevo_estado)
    
    repository_actualizar_estado_pedido(id_pedido, nuevo_estado)
    
    pedido_actualizado = obtener_pedido_por_id(id_pedido)
    return pedido_actualizado
        
def validar_transicion_estado(estado_actual, nuevo_estado):
    
    transiciones_permitidas = {
    "pendiente": ["en_preparacion", "cancelado"],
    "en_preparacion": ["listo", "cancelado"],
    "listo": ["entregado"],
    "entregado": [],
    "cancelado": []
            }
    
    if not estado_actual:
        raise ValidationError("Estado actual invalido")
    
    if nuevo_estado not in transiciones_permitidas:
        raise ValidationError("Estado nuevo invalido")
    
    destinos_validos = transiciones_permitidas[estado_actual]
    
    if nuevo_estado not in destinos_validos:
        raise PedidoInvalidError("transicion no permitida")
    
    return True


def listar_pedidos(
    id_negocio: int, 
    estado: str | None = None, 
    fecha_desde: datetime | None = None,
    fecha_hasta: datetime | None = None,
    limit: int = 10,
    offset: int = 0
    ):
    
    
    
    negocio = obtener_negocio_por_id(id_negocio)
    if not negocio:
        raise NegocioNoEncontradoError("Negocio no encontrado")

    if estado is not None and estado not in ESTADOS_PEDIDO_VALIDOS:
        raise ValidationError(f"estado invalido: {estado}")
      #validar limit:
    if limit <= 0:
            raise ValidationError("Numero de limite invalido")
    if limit > MAX_LIMIT:
            raise ValidationError("Su supero el limite maximo")
        #validar offset:
    if offset < 0: 
            raise ValidationError("offset invalido")
    
    if fecha_desde and fecha_hasta:
        #validar fechas:
        if fecha_desde > fecha_hasta:
            raise ValidationError("fechas invalidas")
        
    pedidos = obtener_pedidos(id_negocio, estado,fecha_desde,fecha_hasta,limit,offset)
    total = contar_pedidos(id_negocio,estado,fecha_desde,fecha_hasta)
    has_next = offset + limit < total
    total_pages = (total + limit - 1) // limit
    
    if total_pages == 0:
        total_pages = 0
        
    
    respuesta = {
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_next": has_next,
        "total_pages":total_pages,
        "items": pedidos
    }
    
    return respuesta

def obtener_pedido_detalle(id_pedido):
    
    
    if id_pedido is None:
        raise ValidationError("El id del pedido es obligatorio")
    
    pedido = obtener_pedido_por_id(id_pedido)
    if not pedido:
        raise PedidoNoEncontradoError("No se encontro el pedido")
    items = obtener_items_por_pedido(id_pedido)
    pedido["items"] = items
    return pedido

