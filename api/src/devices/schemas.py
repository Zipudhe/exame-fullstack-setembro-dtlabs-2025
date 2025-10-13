from datetime import datetime
from typing import Annotated, Optional
from uuid import uuid4

from fastapi import Form
from pydantic import BaseModel, Field


class HearBeat(BaseModel):
    cpu_usage: float
    ram_usage: float
    free_disk: float
    temperature: float
    connectivity: bool
    latency: float


class Device(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    location: str
    sn: str = Field(pattern="^\\d{12}$", min_length=12, max_length=12)
    description: str
    status: list[HearBeat] = []
    boot_date: str = Field(default_factory=lambda: datetime.now().isoformat())
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class DeviceSummary(BaseModel):
    id: str = Field()
    name: str
    location: str
    sn: str
    description: str
    status: Optional[HearBeat] = None
    created_at: str
    updated_at: str


class SummaryList(BaseModel):
    data: Optional[list[DeviceSummary]] = []


class DeviceDetails(BaseModel):
    id: str = Field()
    name: str
    location: str
    sn: str
    description: str
    status: Optional[list[HearBeat]] = []
    created_at: str
    updated_at: str


class DeviceCreated(BaseModel):
    id: str = Field()


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    rebooted: Optional[bool] = None
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


DeviceForm = Annotated[Device, Form()]
