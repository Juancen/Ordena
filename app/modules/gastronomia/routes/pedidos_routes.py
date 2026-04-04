from fastapi import APIRouter, HTTPException
from app.modules.gastronomia.schemas.pedido_schema import PedidoCreate
from app.modules.gastronomia.schemas.pedido_schema import (PedidoResponse,ActualizarEstadoPedido,PedidoEstadoResponse)
from app.modules.gastronomia.services.pedidos_service import (
    consultar_pedido_por_codigo_publico,
    crear_pedido,
    actualizar_estado_pedido,
    listar_pedidos,
    obtener_pedido_detalle
    )
from app.modules.gastronomia.exceptions.pedidos_errors import (
    ValidationError,
    PedidoInvalidError,
    NegocioNoEncontradoError,
    ProductosNoEncontradosError,
    ProductoNoPerteneceAlNegocioError,
    DatabaseError,
    PedidoNoEncontradoError
)

router = APIRouter()

@router.post("/pedidos")
def crear_pedido_endpoint(pedido: PedidoCreate):
    try:
        resultado = crear_pedido(
            id_negocio=pedido.id_negocio,
            nombre_cliente=pedido.nombre_cliente,
            contacto_cliente=pedido.contacto_cliente,
            direccion_cliente=pedido.direccion_cliente,
            tipo_entrega=pedido.tipo_entrega,
            origen=pedido.origen,
            items_pedido=[item.model_dump() for item in pedido.items_pedido]
        )

        return resultado

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PedidoInvalidError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except NegocioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ProductosNoEncontradosError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ProductoNoPerteneceAlNegocioError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    
@router.get("/pedidos/codigo/{codigo_publico}",response_model=PedidoResponse)
def obtener_pedido_por_codigo(codigo_publico: str):
    try:
        return consultar_pedido_por_codigo_publico(codigo_publico)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PedidoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    
@router.patch("/pedidos/{id_pedido}/estado", response_model=PedidoEstadoResponse)
def actualizar_estado(id_pedido: int, data: ActualizarEstadoPedido):
    
    try:
        return actualizar_estado_pedido(id_pedido,data.estado)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PedidoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.get("/negocios/{id_negocio}/pedidos")
def listar_pedidos_route(id_negocio: int, estado: str | None = None):
    try:
        pedidos = listar_pedidos(id_negocio, estado)
        return pedidos

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except NegocioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/pedidos/{id_pedido}")
def detalle_pedido(id_pedido: int):
    
    try:
        pedido = obtener_pedido_detalle(id_pedido)
        return pedido

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PedidoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")