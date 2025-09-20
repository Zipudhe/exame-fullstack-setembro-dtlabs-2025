import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src.database import get_redis_storage

logger = logging.getLogger(__name__)


class UserIdAppend(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if (
            path.startswith("/api/users")
            or path.startswith("/docs")
            or path.startswith("/openapi.json")
        ):
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
