import logging

from pydantic import ValidationError
from typing import Annotated
from src.devices.dependencies import DevicesCollectionDep
from src.devices.schemas import Device
from src.schemas import EntityService
from fastapi import Depends


logger = logging.getLogger(__name__)


class DeviceService(EntityService):
    def __init__(self, collection: DevicesCollectionDep):
        super().__init__(collection)

    def find_one(self, query):
        return super().find_one(query)

    def find_all(self, commons={}, query=None) -> list:
        return super().find_all(commons, query)

    def create(self, payload: Device, user_id: str):
        sn_exists = self.collection.find_one({"user_id": user_id, "sn": payload.sn})

        if sn_exists:
            raise ValidationError("Device already exists")

        self.collection.insert_one({**payload.model_dump(), "user_id": user_id})

        return payload.id

    def delete(self, id: str, user_id: str):
        self.collection.delete_one({"id": id, "user_id": user_id})
        return id


DeviceEngine = Annotated[EntityService, Depends(DeviceService)]
