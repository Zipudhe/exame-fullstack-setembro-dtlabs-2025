from datetime import date, time
from pydantic import BaseModel
from typing import Optional


class Device(BaseModel):
    uuid: str
    name: str
    location: str
    sn: str
    description: str
    user_id: str
    created_at: time
    updated_at: time


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
