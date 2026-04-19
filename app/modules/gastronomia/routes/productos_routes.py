from fastapi import APIRouter, HTTPException
from app.modules.gastronomia.schemas.producto_schema import (
    ProductoCreate,
    ProductoResponse,
    ProductoEstadoUpdate,
    ProductoUpdate,
    MensajeResponse
    )
from app.modules.gastronomia.services.productos_service import (
crear_producto,
listar_productos,
actualizar_estado_service,
editar_producto
)
from app.modules.gastronomia.exceptions.pedidos_errors import (
    ValidationError,
    NegocioNoEncontradoError,
    DatabaseError,
    ProductosNoEncontradosError
    )

router = APIRouter()

@router.post("/productos", response_model=ProductoResponse)
def crear_producto_route(producto: ProductoCreate):
    try:
        nuevo_producto = crear_producto(
            id_negocio=producto.id_negocio,
            nombre=producto.nombre,
            precio=producto.precio
        )
        return nuevo_producto

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except NegocioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
    
@router.get("/negocios/{id_negocio}/productos", response_model=list[ProductoResponse])
def listar_productos_por_negocio(id_negocio:int):
    
    try:
        lista_productos = listar_productos(id_negocio)
        
        return lista_productos
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except NegocioNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.patch("/productos/{id_producto}/estado")
def actualizar_estado_producto(id_producto:int, estado:str):
    
    try:
        producto_desactivado = actualizar_estado_service(id_producto,estado)
        
        return producto_desactivado
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ProductosNoEncontradosError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.put("/productos/{id_producto}",response_model=MensajeResponse)
def editar_producto_route(id_producto:int, producto : ProductoUpdate):
    
    try:
        return editar_producto(
            id_producto=id_producto,
            nombre=producto.nombre,
            precio=producto.precio
    )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")