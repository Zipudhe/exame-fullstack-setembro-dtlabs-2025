import pytest
import logging

from main import app
from src.database import get_db_client, get_database
from pymongo.database import Database
from fastapi.testclient import TestClient


client = TestClient(app)
logger = logging.getLogger(__name__)


def get_database_override():
    client = get_db_client()
    return Database(client, "test_database")


app.dependency_overrides[get_database] = get_database_override


@pytest.fixture()
def users_collection():
    return get_database_override().get_collection("users")


@pytest.fixture(autouse=True)
def database_cleanup():
    yield

    print("TEARDOWN STARTED....\n")
    client = get_db_client()
    client.drop_database("test_database")
    print("TEARDOWN COMPLETE\n")


@pytest.fixture()
def created_user_id():
    user_credentials = {
        "username": "testuser",
        "password": "VerySecurepassword123",
    }

    response = client.post("/api/users", data=user_credentials)
    assert response.status_code == 201
    yield response.json()["id"]


def test_create_device(created_user_id):
    mocked_device = {
        "name": "Temperature Sensor",
        "location": "Warehouse 1",
        "sn": "123456789102",
        "description": "Monitors temperature",
        "user_id": created_user_id,
    }
    response = client.post("/api/devices", data=mocked_device)

    assert response.status_code == 201
