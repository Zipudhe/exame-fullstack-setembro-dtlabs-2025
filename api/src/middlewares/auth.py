import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .constants import public_routes

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(route) for route in public_routes):
            return await call_next(request)

        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return await call_next(request)
