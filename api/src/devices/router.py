import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import ServerSelectionTimeoutError

from .dependencies import DevicesCollectionDep, DevicesQueryParamsDep
from .schemas import Device, DeviceCreated, DeviceForm, DeviceOut, DeviceUpdateForm

router = APIRouter(prefix="/devices", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=Optional[list[DeviceOut]])
async def get_devices(commons: DevicesQueryParamsDep, collection: DevicesCollectionDep):
    logger.info(f"query_param: {commons['q']}")
    try:
        devices = (
            collection.find(commons["q"]).skip(commons["skip"]).limit(commons["limit"])
        )
        logger.debug(f"Retrieved devices: {devices}")
    except ServerSelectionTimeoutError as db_err:
        logger.error(f"Database connection error: {db_err}")
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve devices")

    return devices


@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: str, collection: DevicesCollectionDep):
    return collection.find_one({"uuid": device_id})


@router.get("/{device_id}/status", response_model=Device)
async def get_device_status(device_id: str, collection: DevicesCollectionDep):
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
