import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import ServerSelectionTimeoutError

from .dependencies import (
    DevicesCollectionDep,
    DevicesQueryParamsDep,
)
from .schemas import (
    DeviceCreated,
    DeviceForm,
    DeviceOut,
    DeviceStatus,
    DeviceStatusInput,
    DeviceUpdateForm,
)

router = APIRouter(prefix="/devices", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=Optional[list[DeviceOut]])
async def get_devices(commons: DevicesQueryParamsDep, collection: DevicesCollectionDep):
    try:
        devices = (
            collection.find(commons["q"])
            .skip(commons["skip"])
            .limit(commons["limit"])  # TODO Limit heartbeat to most recent one
        )
        return devices
    except ServerSelectionTimeoutError as db_err:
        logger.error(f"Database connection error: {db_err}")
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve devices")


@router.get("/{device_id}", response_model=DeviceOut)
async def get_device(
    request: Request, device_id: str, collection: DevicesCollectionDep
):
    # TODO: return queried Heartbeat
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
                "user_id": 1,
                "status": {
                    "$arrayElemAt": ["$status", 0],
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


@router.get("/{device_sn}/status", response_model=list[DeviceStatus])
async def get_device_status(
    device_sn: str,
    request: Request,
    devices_collection: DevicesCollectionDep,
    commons: DevicesQueryParamsDep,
):
    user_id = request.state.user_id

    pipeline = [
        {
            "$match": {"sn": device_sn, "user_id": user_id},
        },
        {
            "$project": {
                "_id": 0,
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
        statuses = devices_collection.aggregate(pipeline)  # Revisar schema de saida

        if not statuses:
            return []

        status_list = statuses.to_list()[0]["status"]
        return status_list

    except Exception as e:
        logger.error(f"Error retrieving device status: {e}")
        raise HTTPException(500, "Failed to get device status") from e


@router.post("/{device_sn}/status", status_code=status.HTTP_201_CREATED)
def create_device_status(
    device_sn: str,
    request: Request,
    device_status: DeviceStatusInput,
    devices_collection: DevicesCollectionDep,
):
    user_id = request.state.user_id
    new_status = device_status.model_dump()

    try:
        devices_collection.update_one(
            {"sn": device_sn, "user_id": user_id},
            {"$push": {"status": {"$each": [new_status], "$position": 0}}},
        )

    except Exception as e:
        logger.error(f"Error creating device status: {e}")
        raise HTTPException(
            status_code=500, detail="Unable to create device status"
        ) from e

    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeviceCreated)
async def create_device(
    device: DeviceForm, request: Request, collection: DevicesCollectionDep
):
    try:
        new_device = device.model_dump()
        new_device["user_id"] = request.state.user_id

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
    device: DeviceUpdateForm,
    collection: DevicesCollectionDep,
    request: Request,
):
    user_id = request.state.user_id
    update_values = device.model_dump(exclude_unset=True)
    filter = {"user_id": user_id, "id": device_id}

    try:
        collection.update_one(filter, {"$set": update_values})
    except Exception as e:
        logger.error(f"Error updating device: {device_id}\n detail: {e}")
        raise HTTPException(status_code=400, detail="Unable to update device") from e

    return
