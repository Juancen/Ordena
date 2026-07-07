from backend.app.db.connection import get_connection
from backend.app.db.database import SessionLocal


def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()



def get_db_orm():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()