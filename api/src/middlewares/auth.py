import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if (
            path.startswith("/api/users")
            or path.startswith("/docs")
            or path.startswith("/openapi.json")
        ):
            return await call_next(request)

        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return await call_next(request)
