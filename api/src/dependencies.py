from typing import Annotated
from fastapi import Depends

from src.database import get_database, get_redis_storage
from pymongo.database import Database
from redis import Redis

DatabaseDep = Annotated[Database, Depends(get_database)]

RedisDep = Annotated[Redis, Depends(get_redis_storage)]
