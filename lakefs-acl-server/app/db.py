import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# По умолчанию SQLite, но можно задать любой URI через DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./acl_server.db")

# Для SQLite: extra args для совместимости с несколькими потоками
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
