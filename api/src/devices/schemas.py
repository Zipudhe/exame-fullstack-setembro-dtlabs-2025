from uuid import uuid4

from datetime import datetime
from fastapi import Form
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional


class HearBeat(BaseModel):
    cpu_usage: Optional[int] = None
    ram_usage: Optional[int] = None
    free_disk: Optional[int] = None
    temperature: Optional[float] = None
    latency: Optional[int] = None


class Device(BaseModel):
    _id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    location: str
    sn: str = Field(pattern="^\\d{12}$", min_length=12, max_length=12)
    description: str
    user_id: Optional[str] = None
    status: list[HearBeat] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class DeviceOut(BaseModel):
    _id: str
    name: str
    location: str
    sn: str
    description: str
    user_id: str
    created_at: str
    updated_at: str


class DeviceStatusOut(HearBeat):
    _id: str
    conectivity: bool
    boot_date: str
    created_at: str


class DeviceStatus(HearBeat):
    device_sn: str
    conectivity: bool
    boot_date: str = Field()
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator("boot_date")
    def validate_boot_date(cls, value):
        try:
            date = datetime.fromisoformat(value).date().isoformat()
            return date
        except ValueError as e:
            raise ValueError("boot_date must be in ISO format (YYYY-MM-DD)") from e


class DeviceCreated(BaseModel):
    _id: str


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


DeviceForm = Annotated[Device, Form()]
DeviceUpdateForm = Annotated[DeviceUpdate, Form()]
