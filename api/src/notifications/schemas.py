import logging
from uuid import uuid4
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated, List, Optional

from ..devices.schemas import HearBeat

logger = logging.getLogger(__name__)


class ThreshHoldConfig(HearBeat):
    watch_keys: List[str]

    @field_validator("watch_keys")
    def watch_keys_validator(cls, value):
        for key in value:
            if key not in HearBeat.model_fields.keys():
                raise ValueError("all keys must be a attribute of heart beat")

        return value

    @model_validator(mode="after")
    def check_keys_in_threshhold(self):
        dict_self = self.model_dump()
        logger.info(f"model: {dict_self}")
        for key in dict_self.get("watch_keys", []):
            if not dict_self.get(key):
                raise ValueError(f"threshHold for {key} must be provided")

        return self


class Notification(BaseModel):
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class NotificationConfig(BaseModel):
    _id: str = Field(default_factory=lambda: uuid4().hex)
    device_id: str
    threshHold: ThreshHoldConfig
    notifications: list[Notification] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())


NotificationConfigForm = Annotated[NotificationConfig, Form()]


class NotificationConfigOut(BaseModel):
    _id: str
    device_id: str
    user_id: str
    threshHold: ThreshHoldConfig
    created_at: datetime
    updated_at: datetime


class NotificationConfigUpdate(BaseModel):
    device_id: Optional[str] = None
    threshHold: Optional[ThreshHoldConfig] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
