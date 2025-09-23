from datetime import datetime

from typing import Annotated
from fastapi import Depends
from pymongo.collection import Collection
from src.schemas import DatabaseDep


def get_devices_collection(db: DatabaseDep) -> Collection:
    devices_collection = db.get_collection("devices")
    return devices_collection


def get_devices_query_params(
    location: str = "",
    uuid: str = "",
    sn: str = "",
    skip: int = 0,
    limit: int = 100,
    created_at: str = "",
):
    q = dict()
    if location:
        q.update({"location": location})

    if uuid:
        q.update({"uuid": uuid})

    if sn:
        q.update({"sn": sn})

    if created_at:
        q.update({"creatd_at": datetime.fromisoformat(created_at).date().isoformat()})

    return {"q": q, "skip": skip, "limit": limit}


DevicesCollectionDep = Annotated[Collection, Depends(get_devices_collection)]

DevicesQueryParamsDep = Annotated[dict, Depends(get_devices_query_params)]
