import logging
import re
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src.database import get_redis_storage
from .constants import public_routes

logger = logging.getLogger(__name__)


class UserIdAppend(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path == "/" or any(path.startswith(route) for route in public_routes):
            return await call_next(request)

        if (
            re.fullmatch(
                r"/api/devices/([a-z0-9]){32}/status",
                path,
            )
            and request.method == "POST"
        ):
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        redis_store = get_redis_storage()
        session_id = request.cookies.get("session_id")

        if not session_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_id = redis_store.get(f"userSession:{session_id}")

        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        request.state.user_id = user_id

        return await call_next(request)
