from fastapi import FastAPI
from app.modules.turnos.routers.turno import router as router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Ordena API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)