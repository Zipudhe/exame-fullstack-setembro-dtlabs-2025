import logging
from typing import Optional
from pymongo.errors import ServerSelectionTimeoutError

from fastapi import APIRouter, status, HTTPException
from src.schemas import CommonsDep
from .dependencies import DevicesCollectionDep

from .schemas import Device, DeviceOut, DeviceCreated, DeviceForm

router = APIRouter(prefix="/devices", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=Optional[list[DeviceOut]])
async def get_devices(commons: CommonsDep, collection: DevicesCollectionDep):
    try:
        devices = collection.find()
        logger.debug("Retrieved devices: %s", devices)
    except ServerSelectionTimeoutError as db_err:
        logger.error(f"Database connection error: {db_err}")
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve devices")

    return devices


@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: str):
    return


@router.get("/{device_id}/status", response_model=Device)
async def get_device_status(device_id: str, commons: CommonsDep):
    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeviceCreated)
async def create_device(device: DeviceForm, collection: DevicesCollectionDep):
    try:
        collection.insert_one(device.model_dump())
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail="Unable to create device") from e

    return device.model_dump()


@router.delete("/{device_id}")
async def delete_device(device_id: str):
    return


@router.put("/{device_id}")
async def update_device(device_id: str, device: Device):
    return
