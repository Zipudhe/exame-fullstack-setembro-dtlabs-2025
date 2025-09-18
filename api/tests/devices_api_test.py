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
def user_cookies(user_credentials):
    response = client.post("/api/users/login", data=user_credentials)

    yield response.cookies


@pytest.fixture()
def user_credentials():
    user_credentials = {
        "username": "testuser",
        "password": "VerySecurepassword123",
    }

    response = client.post("/api/users", data=user_credentials)
    assert response.status_code == 201
    yield user_credentials


@pytest.fixture()
def created_user_id():
    user_credentials = {
        "username": "testuser",
        "password": "VerySecurepassword123",
    }

    response = client.post("/api/users", data=user_credentials)
    assert response.status_code == 201
    yield response.json()["id"]


@pytest.fixture()
def created_device(user_cookies):
    mocked_device = {
        "name": "Temperature Sensor",
        "location": "Warehouse 1",
        "sn": "123456789102",
        "description": "Monitors temperature",
    }
    response = client.post("/api/devices", data=mocked_device, cookies=user_cookies)

    assert response.status_code == 201

    created_device_id = response.json()

    mocked_device.update({"uuid": created_device_id["uuid"]})
    yield mocked_device


def test_create_device(user_cookies):
    mocked_device = {
        "name": "Temperature Sensor",
        "location": "Warehouse 1",
        "sn": "123456789102",
        "description": "Monitors temperature",
    }
    response = client.post("/api/devices", data=mocked_device, cookies=user_cookies)

    assert response.status_code == 201


@pytest.fixture()
def create_multiple_devices(user_cookies):
    mocked_device_1 = {
        "name": "Temperature Sensor",
        "location": "Warehouse 1",
        "sn": "123456789102",
        "description": "Monitors temperature",
    }
    mocked_device_2 = {
        "name": "Temperature light",
        "location": "Warehouse 2",
        "sn": "123456789101",
        "description": "Monitors light",
    }
    mocked_device_3 = {
        "name": "Temperature motion",
        "location": "Warehouse 1",
        "sn": "123456789103",
        "description": "Monitors motion",
    }

    devices = [mocked_device_1, mocked_device_2, mocked_device_3]
    for device in devices:
        response = client.post("/api/devices", data=device, cookies=user_cookies)
        assert response.status_code == 201

    yield devices


def test_list_devices(created_device, user_cookies):
    response = client.get("/api/devices", cookies=user_cookies)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    device = data[0]

    assert device["sn"] == created_device["sn"]


def test_multiple_devices(create_multiple_devices, user_cookies):
    response = client.get("/api/devices", cookies=user_cookies)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3


def test_query_devices(create_multiple_devices, user_cookies):
    expected_location = "Warehouse 2"
    response = client.get(
        "/api/devices",
        cookies=user_cookies,
        params={"location": expected_location},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    device = data[0]

    assert device["location"] == expected_location


def test_get_single_device(created_device, user_cookies):
    expected_sn = created_device["sn"]

    response = client.get(
        f"/api/devices/{created_device['uuid']}",
        cookies=user_cookies,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sn"] == expected_sn


def test_delete_device(created_device, user_cookies):
    response = client.delete(
        f"/api/devices/{created_device['uuid']}",
        cookies=user_cookies,
    )

    assert response.status_code == 200


def test_update_device(created_device, user_cookies):
    expected_location = "Warehouse 3"
    device_uuid = created_device["uuid"]

    update_device = {"location": expected_location}

    response = client.put(
        f"/api/devices/{device_uuid}", cookies=user_cookies, data=update_device
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/devices/{device_uuid}",
        cookies=user_cookies,
    )

    updated_device = get_response.json()

    assert updated_device["location"] == expected_location
