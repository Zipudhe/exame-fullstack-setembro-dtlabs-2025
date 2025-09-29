import logging

from datetime import datetime
from bson import ObjectId
from fastapi import Form
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
)
from typing import Annotated, List, Optional

from ..devices.schemas import HearBeat

logger = logging.getLogger(__name__)

PyObjectId = Annotated[
    str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)
]


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
    user_id: str
    threshHold: ThreshHoldConfig
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())


NotificationConfigForm = Annotated[NotificationConfig, Form()]


class NotificationConfigOut(BaseModel):
    id: PyObjectId = Field(validation_alias="_id")
    user_id: str
    threshHold: ThreshHoldConfig
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        validate_by_alias=True, validate_by_name=True, json_encoders={ObjectId: str}
    )


class NotificationConfigUpdate(BaseModel):
    threshHold: Optional[ThreshHoldConfig] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
