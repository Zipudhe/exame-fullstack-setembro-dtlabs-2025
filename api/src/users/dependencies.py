from typing import Annotated
from fastapi import Depends
from pymongo.collection import Collection
from src.schemas import DatabaseDep


def get_user_collection(db: DatabaseDep) -> Collection:
    user_collection = db.get_collection("users")

    return user_collection


UserCollectionDep = Annotated[Collection, Depends(get_user_collection)]
