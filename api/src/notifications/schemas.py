from datetime import date
from pydantic import BaseModel, field_validator
from typing import List

from devices.schemas import HearBeat


class ThreshHoldConfig(HearBeat):
    watch_keys: List[str]

    @field_validator("watch_keys")
    def watch_keys_validator(cls, value):
        for key in value:
            if key not in HearBeat.model_fields.keys():
                raise ValueError("all keys must be a attribute of heart beat")


class Notification(BaseModel):
    uuid: str
    threshHold: ThreshHoldConfig
    created_at: date
    updated_at: date
