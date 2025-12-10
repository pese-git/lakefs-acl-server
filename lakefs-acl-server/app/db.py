import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Поддержка shared in-memory SQLite для тестов (один engine для всех сессий)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./acl_server.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # Позволяет использовать shared in-memory базу:
    if DATABASE_URL == "sqlite:///:memory:" or DATABASE_URL.startswith("sqlite:///:memory:?cache=shared"):
        DATABASE_URL = "sqlite:///:memory:?cache=shared"
        connect_args = {"check_same_thread": False, "uri": True}
    else:
        connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
