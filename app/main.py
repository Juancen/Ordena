from fastapi import FastAPI
from app.modules.gastronomia.routes.pedidos_routes import router as pedidos_router

app = FastAPI(title="Ordena API")

app.include_router(pedidos_router)