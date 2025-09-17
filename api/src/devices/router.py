from fastapi import APIRouter, status

from schemas import Device
from src.schemas import CommonsDep

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[Device])
async def get_devices():
    return {"data": []}


@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: str):
    return


@router.get("/{device_id}/status", response_model=Device)
async def get_device_status(device_id: str, commons: CommonsDep):
    return


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_device(device: Device):
    return


@router.delete("/{device_id}")
async def delete_device(device_id: str):
    return


@router.put("/{device_id}")
async def update_device(device_id: str, device: Device):
    return
