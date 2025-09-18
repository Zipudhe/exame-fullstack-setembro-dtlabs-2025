from uuid import uuid4

from datetime import datetime, date
from fastapi import Form
from pydantic import BaseModel, Field
from typing import Annotated, Optional


class Device(BaseModel):
    uuid: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    location: str
    sn: str = Field(pattern="^\\d{12}$", min_length=12, max_length=12)
    description: str
    user_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class DeviceOut(BaseModel):
    uuid: str
    name: str
    location: str
    sn: str
    description: str
    user_id: str
    created_at: str
    updated_at: str


class HearBeat(BaseModel):
    cpu_usage: Optional[int] = None
    ram_usage: Optional[int] = None
    free_disk: Optional[int] = None
    tempeture: Optional[float] = None
    latency: Optional[int] = None


class DeviceStatus(HearBeat):
    device_id: str
    conectivity: bool
    boot_date: date


class DeviceCreated(BaseModel):
    uuid: str


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


DeviceForm = Annotated[Device, Form()]
DeviceUpdateForm = Annotated[DeviceUpdate, Form()]
