from datetime import datetime, timezone

from typing import Annotated
from fastapi import Depends
from pymongo.collection import Collection
from src.dependencies import DatabaseDep


def get_devices_collection(db: DatabaseDep) -> Collection:
    devices_collection = db.get_collection("devices")
    return devices_collection


def get_devices_query_params(
    location: str = "",
    uuid: str = "",
    sn: str = "",
    skip: int = 0,
    limit: int = 100,
    start_date: str = "",
    end_date: str = "",
):
    q = dict()
    if location:
        q.update({"location": location})

    if uuid:
        q.update({"uuid": uuid})

    if sn:
        q.update({"sn": sn})

    if start_date:
        q.update(
            {
                "start_date": {
                    "$gte": [
                        {
                            "$toDate": "$$item.created_at"
                        },  # Convert to Date for comparison
                        datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc),
                    ]
                }
            }
        )

    if end_date:
        q.update(
            {
                "end_date": {
                    "$lte": [
                        {
                            "$toDate": "$$item.created_at"
                        },  # Convert to Date for comparison
                        datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc),
                    ]
                }
            }
        )

    return {
        "q": q,
        "skip": skip,
        "limit": limit,
    }


DevicesCollectionDep = Annotated[Collection, Depends(get_devices_collection)]

DevicesQueryParamsDep = Annotated[dict, Depends(get_devices_query_params)]
