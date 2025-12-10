from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.users import router as users_router
from app.auth import TokenAuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Create tables in DB on startup (no Alembic needed yet) ---
    from app.db import engine
    from app.models import Base

    Base.metadata.create_all(bind=engine)
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
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # Переопределить openapi-генератор  # ty:ignore[invalid-assignment]

app.add_middleware(
    TokenAuthMiddleware, allowed_paths=["/health", "/docs", "/openapi.json", "/redoc"]
)  # type: ignore
app.include_router(users_router)


@app.get("/health", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
