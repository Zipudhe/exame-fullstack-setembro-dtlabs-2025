from fastapi import Depends
from typing import Annotated

from .database import get_database
from pymongo.database import Database


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]

DatabaseDep = Annotated[Database, Depends(get_database)]
