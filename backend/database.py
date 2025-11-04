from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base
from fastapi import HTTPException

DATABASE_URL = "sqlite:///database/database.db"

engine = create_engine(
    url = DATABASE_URL,
    connect_args = {'check_same_thread': False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка при создании таблиц: {e}')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()