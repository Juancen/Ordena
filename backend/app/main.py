from fastapi import FastAPI
from app.modules.turnos.routers.turno import router as router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Ordena API")

from app.db.database import engine, Base
from app.modules.turnos.models.models_turno import Turno
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)