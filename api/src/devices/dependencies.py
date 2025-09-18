from typing import Annotated
from fastapi import Depends
from pymongo.collection import Collection
from src.schemas import DatabaseDep


def get_dependencie_collection(db: DatabaseDep) -> Collection:
    devices_collection = db.get_collection("devices")
    return devices_collection


DevicesCollectionDep = Annotated[Collection, Depends(get_dependencie_collection)]
