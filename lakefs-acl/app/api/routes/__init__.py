from fastapi import FastAPI

from .credentials import router as credentials_router
from .groups import router as groups_router
from .policies import router as policies_router
from .users import router as users_router


def register_routes(app: FastAPI) -> None:
    app.include_router(users_router)
    app.include_router(groups_router)
    app.include_router(policies_router)
    app.include_router(credentials_router)
