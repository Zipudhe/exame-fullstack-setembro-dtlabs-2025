import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import ServerSelectionTimeoutError

from .dependencies import (
    DevicesCollectionDep,
    DevicesQueryParamsDep,
    StatusCollectionDep,
)
from .schemas import (
    Device,
    DeviceCreated,
    DeviceForm,
    DeviceOut,
    DeviceStatus,
    DeviceUpdateForm,
    DeviceStatusOut,
)

router = APIRouter(prefix="/devices", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=Optional[list[DeviceOut]])
async def get_devices(commons: DevicesQueryParamsDep, collection: DevicesCollectionDep):
    try:
        devices = (
            collection.find(commons["q"]).skip(commons["skip"]).limit(commons["limit"])
        )
        return devices
    except ServerSelectionTimeoutError as db_err:
        logger.error(f"Database connection error: {db_err}")
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve devices")


@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: str, collection: DevicesCollectionDep):
    # TODO: Always get most recent status
    return collection.find_one({"uuid": device_id})


@router.get("/{device_sn}/status", response_model=list[DeviceStatusOut])
async def get_device_status(
    device_sn: str,
    request: Request,
    status_collection: StatusCollectionDep,
    devices_collection: DevicesCollectionDep,
    commons: DevicesQueryParamsDep,
):
    user_id = request.state.user_id

    try:
        device = devices_collection.find_one(
            {"sn": device_sn, "user_id": user_id}, {"uuid": 1}
        )

        if not device:
            return []

        logger.info(f"device: {device['uuid']}")

        status = (
            status_collection.find({"device_id": device["uuid"]})
            .skip(commons["skip"])
            .limit(commons["limit"])
        )
        return status
    except Exception as e:
        logger.error(f"Error retrieving device status: {e}")
        raise HTTPException(500, "Failed to get device status") from e


@router.post("/{device_sn}/status", status_code=status.HTTP_201_CREATED)
def create_device_status(
    device_sn: str,
    request: Request,
    device_status: DeviceStatus,
    status_collection: StatusCollectionDep,
    devices_collection: DevicesCollectionDep,
):
    user_id = request.state.user_id

    try:
        device = devices_collection.find_one(
            {"sn": device_sn, "user_id": user_id}, {"uuid": 1}
        )

        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        new_status = device_status.model_dump()
        new_status["device_id"] = device["uuid"]
        status_collection.insert_one(new_status)

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
        collection.delete_one({"uuid": device_id, "user_id": user_id})
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
    filter = {"user_id": user_id, "uuid": device_id}

    try:
        collection.update_one(filter, {"$set": update_values})
    except Exception as e:
        logger.error(f"Error updating device: {device_id}\n detail: {e}")
        raise HTTPException(status_code=400, detail="Unable to update device") from e

    return
