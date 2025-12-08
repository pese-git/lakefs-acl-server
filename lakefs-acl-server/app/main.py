from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.auth import TokenAuthMiddleware

app = FastAPI()
app.add_middleware(TokenAuthMiddleware, allowed_paths=["/health"])  # type: ignore

@app.get("/health", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("lakefs-acl-server.app.main:app", host="0.0.0.0", port=8000, reload=True)
