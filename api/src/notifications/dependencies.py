from typing import Annotated
from fastapi import Depends
from pymongo.collection import Collection
from src.schemas import DatabaseDep


def get_notifications_collection(db: DatabaseDep) -> Collection:
    notifications_collection = db.get_collection("notifications")
    return notifications_collection


def get_notifications_config_collection(db: DatabaseDep) -> Collection:
    notifications_config_collection = db.get_collection("notifications_config")
    return notifications_config_collection


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
        q.update({"creatd_at": created_at})

    return {"q": q, "skip": skip, "limit": limit}


NotificationsCollectionDep = Annotated[
    Collection, Depends(get_notifications_collection)
]
NotificationsConfigCollectionDep = Annotated[
    Collection, Depends(get_notifications_config_collection)
]
