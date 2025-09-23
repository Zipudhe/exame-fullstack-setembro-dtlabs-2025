from datetime import datetime
from typing import Annotated, Optional
from uuid import uuid4

from fastapi import Form
from pydantic import BaseModel, Field, field_validator


class HearBeat(BaseModel):
    cpu_usage: Optional[int] = None
    ram_usage: Optional[int] = None
    free_disk: Optional[int] = None
    temperature: Optional[float] = None
    latency: Optional[int] = None


class DeviceStatus(HearBeat):
    conectivity: bool
    boot_date: str = Field()
    created_at: str


class DeviceStatusInput(HearBeat):
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


class Device(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    location: str
    sn: str = Field(pattern="^\\d{12}$", min_length=12, max_length=12)
    description: str
    status: Optional[list[DeviceStatus]] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class DeviceOut(BaseModel):
    id: str = Field()
    name: str
    location: str
    sn: str
    description: str
    status: list[DeviceStatus] = []
    user_id: str
    created_at: str
    updated_at: str


class DeviceCreated(BaseModel):
    id: str = Field()


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


DeviceForm = Annotated[Device, Form()]
DeviceUpdateForm = Annotated[DeviceUpdate, Form()]
