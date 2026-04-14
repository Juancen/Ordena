from fastapi import APIRouter, HTTPException
from app.modules.gastronomia.schemas.producto_schema import ProductoCreate, ProductoResponse
from app.modules.gastronomia.services.productos_service import (
crear_producto,
listar_productos
)
from app.modules.gastronomia.exceptions.pedidos_errors import (
    ValidationError,
    NegocioNoEncontradoError,
    DatabaseError
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