from fastapi import APIRouter
from app.modules.gastronomia.repositories.pedidos_repository import obtener_productos_por_ids

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

