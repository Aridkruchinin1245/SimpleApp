from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///../database/database.db?mode=rwc"

engine = create_engine(
    url = DATABASE_URL,
    connect_args = {'check_same_thread': False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

