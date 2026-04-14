from app.modules.gastronomia.repositories.negocio_repository import obtener_negocio_por_id
from app.modules.gastronomia.repositories.producto_repository import (
    existe_producto_con_mismo_nombre,
    crear_producto_repository
    )
from app.modules.gastronomia.exceptions.pedidos_errors import (ValidationError,NegocioNoEncontradoError)
from typing import cast
from decimal import Decimal, InvalidOperation


def crear_producto(id_negocio: int, nombre: str, precio: float):
    negocio = obtener_negocio_por_id(id_negocio)

    if negocio is None:
        raise NegocioNoEncontradoError("El negocio no existe")
    
    negocio = cast(dict, negocio)

    if negocio["estado"] != "activo":
        raise ValidationError("El negocio no está activo")

    nombre_limpio = nombre.strip()

    if not nombre_limpio:
        raise ValidationError("El nombre del producto es obligatorio")

    if len(nombre_limpio) < 2:
        raise ValidationError("El nombre del producto debe tener al menos 4 caracteres")

    if precio is None:
        raise ValidationError("El precio es obligatorio")

    try:
        precio_decimal = Decimal(str(precio))
    except (InvalidOperation, ValueError):
        raise ValidationError("El precio no es válido")
    
    if precio_decimal <= 0:
        raise ValidationError("El precio debe ser mayor a 0")

    if existe_producto_con_mismo_nombre(id_negocio, nombre_limpio):
        raise ValidationError("El producto ya existe")

    producto_creado = crear_producto_repository(
        id_negocio=id_negocio,
        nombre=nombre_limpio,
        precio=precio_decimal,
        estado="activo"
    )

    return producto_creado