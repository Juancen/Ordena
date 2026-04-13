from fastapi import FastAPI
from app.modules.gastronomia.routes.pedidos_routes import router as pedidos_router
from app.modules.gastronomia.routes.productos_routes import router as productos_routes
app = FastAPI(title="Ordena API")

app.include_router(productos_routes, prefix="/productos")
app.include_router(pedidos_router, prefix="/gastronomia")