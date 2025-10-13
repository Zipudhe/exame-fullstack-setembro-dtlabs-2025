from abc import ABC, abstractmethod
import logging

from src.devices.dependencies import DevicesQueryParamsDep
from pymongo.collection import Collection

logger = logging.getLogger(__name__)


class EntityService(ABC):
    collection: Collection

    def __init__(self, collection: Collection):
        self.collection = collection

    @abstractmethod
    def find_one(self, query):
        if isinstance(query, dict):
            return self.collection.find_one(query)

        return self.collection.aggregate(query).to_list()[0]

    @abstractmethod
    def find_all(self, commons: DevicesQueryParamsDep = {}, query=None) -> list:
        if not query:
            return self.collection.find(
                filter={}, skip=commons["skip"], limit=commons["limit"]
            ).to_list()

        if isinstance(query, dict):
            return self.collection.find(
                filter=query, skip=commons["skip"], limit=commons["limit"]
            ).to_list()

        return self.collection.aggregate(query).to_list()

    @abstractmethod
    def create(self, payload, user_id: str) -> str:
        pass

    @abstractmethod
    def delete(self, id, user_id: str) -> str:
        pass
