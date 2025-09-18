import logging
from fastapi import Depends
from typing import Annotated

from .database import get_database, get_redis_storage
from pymongo.database import Database
from redis import Redis

logger = logging.getLogger(__name__)


async def common_parameters(
    q: str | None = None, location: str = "", skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]

DatabaseDep = Annotated[Database, Depends(get_database)]

RedisDep = Annotated[Redis, Depends(get_redis_storage)]
