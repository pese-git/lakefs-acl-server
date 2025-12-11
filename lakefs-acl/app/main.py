from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

from fastapi import FastAPI, Response
from fastapi.openapi.utils import get_openapi

from app.api.routes import register_routes
from app.auth.auth import TokenAuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Create tables in DB on startup (no Alembic needed yet) ---
    from app.db.session import SessionLocal, engine
    from app.init_defaults import init_default_groups_and_policies
    from app.models import Base

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    init_default_groups_and_policies(db)
    db.close()
    yield
    # Место для shutdown-кода, если потребуется


app = FastAPI(lifespan=lifespan)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Добавляем bearer-схему для авторизации
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # Переопределить openapi-генератор  # ty:ignore[invalid-assignment]

app.add_middleware(
    TokenAuthMiddleware,
    allowed_paths=[
        "/config/version",
        "/healthcheck",
        "/auth/health",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/favicon.ico",
    ],
)  # type: ignore

register_routes(app)


@app.get("/healthcheck", tags=["Health"])
def health_check():
    return Response(status_code=204)


@app.get("/config/version", tags=["Health"])
def acl_version():
    # Можно подставить свой version build/info
    return JSONResponse(content={"version": "1.0.0"})


@app.get("/auth/health", tags=["Health"])
def health_check_alias():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
