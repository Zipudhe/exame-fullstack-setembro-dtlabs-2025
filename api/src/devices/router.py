import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import ServerSelectionTimeoutError

from src.websocket.stream import publish_to_stream, acknowledge_message

from .dependencies import (
    DevicesCollectionDep,
    DevicesQueryParamsDep,
)
from .schemas import (
    DeviceCreated,
    DeviceForm,
    DeviceDetails,
    DeviceSummary,
    DeviceStatus,
    DeviceStatusInput,
    DeviceUpdate,
)

router = APIRouter(prefix="/devices", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=Optional[list[DeviceSummary]])
async def get_devices(
    request: Request, commons: DevicesQueryParamsDep, collection: DevicesCollectionDep
):
    user_id = request.state.user_id

    pipeline = [
        {"$skip": commons["skip"]},
        {"$limit": commons["limit"]},
        {
            "$match": {
                "user_id": user_id,
            },
        },
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "name": 1,
                "location": 1,
                "sn": 1,
                "description": 1,
                "created_at": 1,
                "updated_at": 1,
                "status": {
                    "$arrayElemAt": ["$status", 0],
                },
            }
        },
    ]
    try:
        return collection.aggregate(
            pipeline,
        ).to_list()
    except ServerSelectionTimeoutError as db_err:
        logger.error(f"Database connection error: {db_err}")
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve devices")


@router.get("/{device_id}", response_model=DeviceDetails)
async def get_device(
    commons: DevicesQueryParamsDep,
    request: Request,
    device_id: str,
    collection: DevicesCollectionDep,
):
    user_id = request.state.user_id
    pipeline = [
        {
            "$match": {"id": device_id, "user_id": user_id},
        },
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "name": 1,
                "location": 1,
                "sn": 1,
                "description": 1,
                "created_at": 1,
                "updated_at": 1,
                "status": {
                    "$slice": [
                        {
                            "$sortArray": {
                                "input": "$status",
                                "sortBy": {"created_at": -1},
                            }
                        },
                        commons["skip"],
                        commons["limit"],
                    ],
                },
            }
        },
    ]

    try:
        device = collection.aggregate(pipeline).to_list()
    except Exception as e:
        logger.error(f"Error retrieving device: {e}")
        raise HTTPException(500, "Failed to get device") from e

    return device[0]


@router.get("/{device_id}/status", response_model=list[DeviceStatus])
async def get_device_status(
    device_id: str,
    request: Request,
    devices_collection: DevicesCollectionDep,
    commons: DevicesQueryParamsDep,
):
    user_id = request.state.user_id

    filter_conditions = []

    if commons["start_date"]:
        start_date = datetime.fromisoformat(commons["start_date"]).replace(
            tzinfo=timezone.utc
        )
        filter_conditions.append(
            {
                "$gte": [
                    {"$toDate": "$$item.created_at"},  # Convert to Date for comparison
                    start_date,
                ]
            }
        )

    if commons["end_date"]:
        end_date = datetime.fromisoformat(commons["end_date"]).replace(
            tzinfo=timezone.utc
        )
        filter_conditions.append(
            {
                "$lte": [
                    {"$toDate": "$$item.created_at"},  # Convert to Date for comparison
                    end_date,
                ]
            }
        )

    if filter_conditions:
        filter_cond = (
            {"$and": filter_conditions}
            if len(filter_conditions) > 1
            else filter_conditions[0]
        )
    else:
        filter_cond = True

    print(f"{filter_cond}")
    pipeline = [
        {
            "$match": {"id": device_id, "user_id": user_id},
        },
        {
            "$addFields": {
                "filtered_status": {
                    "$filter": {
                        "input": "$status",
                        "as": "item",
                        "cond": filter_cond,
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "status": {
                    "$slice": [
                        {
                            "$sortArray": {
                                "input": "$filtered_status",
                                "sortBy": {"created_at": -1},
                            }
                        },
                        commons["skip"],
                        commons["limit"],
                    ],
                },
            }
        },
    ]

    try:
        statuses = devices_collection.aggregate(pipeline)  # Revisar schema de saida

        if not statuses:
            return []

        status_list = statuses.to_list()[0]["status"]
        return status_list

    except Exception as e:
        logger.error(f"Error retrieving device status: {e}")
        raise HTTPException(500, "Failed to get device status") from e


@router.post("/{device_id}/status", status_code=status.HTTP_201_CREATED)
async def create_device_status(
    device_id: str,
    device_status: DeviceStatusInput,
    devices_collection: DevicesCollectionDep,
):
    new_status = device_status.model_dump()

    # await publish_to_stream(user_id, "new notification arrived") should subscribe to device id

    try:
        devices_collection.update_one(
            {"id": device_id},
            {"$push": {"status": {"$each": [new_status], "$position": 0}}},
        )

    except Exception as e:
        logger.error(f"Error creating device status: {e}")
        raise HTTPException(
            status_code=500, detail="Unable to create device status"
        ) from e

    return


@router.post("/ack")
async def ack_device_notification(request: Request, message_id: str):
    user_id = request.state.user_id
    await acknowledge_message(user_id, message_id)
    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeviceCreated)
async def create_device(
    device: DeviceForm, request: Request, collection: DevicesCollectionDep
):
    new_device = device.model_dump(mode="json")
    user_id = request.state.user_id
    sn_exists = collection.find_one({"user_id": user_id, "sn": new_device["sn"]})

    if sn_exists:
        raise HTTPException(
            status_code=400, detail="Device with serial number already exists"
        )

    try:
        new_device["user_id"] = request.state.user_id
        new_device["status"] = []

        collection.insert_one(new_device)
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail="Unable to create device") from e

    return new_device


@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(
    device_id: str, collection: DevicesCollectionDep, request: Request
):
    user_id = request.state.user_id
    try:
        collection.delete_one({"id": device_id, "user_id": user_id})
    except Exception as e:
        logger.error(f"Error deleting device: {device_id}\n detail: {e}")
        raise HTTPException(status_code=400, detail="Unable to delete device") from e
    return


@router.put("/{device_id}", status_code=status.HTTP_200_OK)
async def update_device(
    device_id: str,
    device: DeviceUpdate,
    collection: DevicesCollectionDep,
    request: Request,
):
    user_id = request.state.user_id
    update_values = device.model_dump(exclude_unset=True)
    print(f"{update_values}")
    filter = {"user_id": user_id, "id": device_id}

    try:
        collection.update_one(filter, {"$set": update_values})
    except Exception as e:
        logger.error(f"Error updating device: {device_id}\n detail: {e}")
        raise HTTPException(status_code=400, detail="Unable to update device") from e

    return
