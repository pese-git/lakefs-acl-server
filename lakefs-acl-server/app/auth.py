import os

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

API_TOKEN_ENV = "ACL_API_TOKEN"


def get_api_token() -> str:
    token = os.getenv(API_TOKEN_ENV)
    print("[TRACE] ACL_API_TOKEN from .env:", token)
    if not token:
        raise RuntimeError(
            f"Environment variable {API_TOKEN_ENV} is required for API token protection."
        )
    return token


async def verify_token(request: Request):
    token = get_api_token()
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header.",
        )
    provided_token = auth_header.split(" ", 1)[1].strip()
    if provided_token != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token.")
    return True


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_paths=None):
        super().__init__(app)
        self.token = os.getenv(API_TOKEN_ENV)
        print("[TRACE] ACL_API_TOKEN on middleware init:", self.token)
        if not self.token:
            raise RuntimeError(
                f"Environment variable {API_TOKEN_ENV} is required for API token protection."
            )
        self.allowed_paths = allowed_paths if allowed_paths is not None else ["/health"]

    async def dispatch(self, request: Request, call_next):
        print("[TRACE] Incoming request path:", request.url.path)
        if request.url.path in self.allowed_paths:
            print("[TRACE] Path allowed without token.")
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        print("[TRACE] Authorization header:", auth_header)
        if not auth_header or not auth_header.startswith("Bearer "):
            print("[TRACE] Missing or invalid authorization header!")
            return Response(content="Missing or invalid authorization header.", status_code=401)
        provided_token = auth_header.split(" ", 1)[1].strip()
        print("[TRACE] Provided token:", provided_token)
        if provided_token != self.token:
            print("[TRACE] Invalid token!")
            return Response(content="Invalid API token.", status_code=401)
        print("[TRACE] Token matched!")
        return await call_next(request)
