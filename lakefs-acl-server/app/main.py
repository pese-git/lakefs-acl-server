from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.auth import TokenAuthMiddleware

app = FastAPI()
app.add_middleware(TokenAuthMiddleware, allowed_paths=["/health"])  # type: ignore


# --- Create tables in DB on startup (no Alembic needed yet) ---
@app.on_event("startup")
def on_startup():
    from app.db import engine
    from app.models import Base

    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
