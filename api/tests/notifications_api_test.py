import logging

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from main import app
from pymongo.database import Database
from src.database import get_database, get_db_client

client = TestClient(app)
logger = logging.getLogger(__name__)


def get_database_override():
    client = get_db_client()
    return Database(client, "test_database")


app.dependency_overrides[get_database] = get_database_override


@pytest.fixture()
def created_device(user_cookies):
    mocked_device = {
        "name": "Temperature Sensor",
        "location": "Warehouse 1",
        "sn": "123456789102",
        "description": "Monitors temperature",
    }

    response = client.post("/api/devices", data=mocked_device)

    assert response.status_code == 201

    created_device_id = response.json()

    mocked_device.update({"uuid": created_device_id["uuid"]})
    yield mocked_device

    client.delete(f"/api/devices/{created_device_id['uuid']}")


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
def created_config(user_cookies, created_device):
    mocked_config = {
        "device_id": created_device["uuid"],
        "threshHold": {
            "watch_keys": ["cpu_usage"],
            "cpu_usage": 30,
        },
    }

    response = client.post("/api/notifications/config", json=mocked_config)

    assert response.status_code == 201

    created_config_id = response.json()

    mocked_config.update({"uuid": created_config_id["uuid"]})
    yield mocked_config

    client.delete(f"/api/notifications/config/{created_config_id['uuid']}")


@pytest.fixture()
def user_cookies(user_credentials):
    response = client.post("/api/users/login", data=user_credentials)

    session_id = response.cookies.get("session_id")
    logger.info(f"session_id: {session_id}")
    if session_id:
        client.cookies.set("session_id", session_id)

    yield

    client.cookies.clear()


@pytest.fixture()
def user_credentials():
    user_credentials = {
        "username": "testuser",
        "password": "VerySecurepassword123",
    }

    response = client.post("/api/users", data=user_credentials)
    assert response.status_code == 201
    yield user_credentials


def test_create_notification_config(user_cookies, created_device):
    mocked_config = {
        "device_id": created_device["uuid"],
        "threshHold": {
            "watch_keys": ["cpu_usage"],
            "cpu_usage": 30,
        },
    }

    response = client.post("/api/notifications/config", json=mocked_config)

    assert response.status_code == 201


@pytest.fixture()
def create_multiple_notifications(user_cookies, created_device):
    mocked_notification_1 = {
        "device_id": created_device["uuid"],
        "threshHold": {
            "watch_keys": ["cpu_usage"],
            "cpu_usage": 30,
        },
    }

    mocked_notification_2 = {
        "device_id": created_device["uuid"],
        "threshHold": {
            "watch_keys": ["cpu_usage", "ram_usage"],
            "cpu_usage": 30,
            "ram_usage": 70,
        },
    }
    mocked_notification_3 = {
        "device_id": created_device["uuid"],
        "threshHold": {"watch_keys": ["temperature"], "temperature": 75.5},
    }

    notifications = [
        mocked_notification_1,
        mocked_notification_2,
        mocked_notification_3,
    ]

    for notification in notifications:
        response = client.post("/api/notifications/config", json=notification)
        assert response.status_code == 201

    yield notifications


def test_multiple_notifications(create_multiple_notifications):
    excpected_count = 3

    configs = client.get("/api/notifications/config").json()

    assert len(configs) == excpected_count


def test_delete_notification(create_multiple_notifications):
    to_delete = client.get("/api/notifications/config").json()[0]["uuid"]
    excpected_count = len(create_multiple_notifications) - 1

    response = client.delete(f"/api/notifications/config/{to_delete}")

    assert response.status_code == 204

    notifications = client.get("/api/notifications/config").json()

    assert len(notifications) == excpected_count


def test_update_notification(create_multiple_notifications):
    to_update = client.get("/api/notifications/config").json()[0]
    config_id = to_update["uuid"]

    updated_config = {
        **to_update,
        "threshHold": {**to_update["threshHold"], "cpu_usage": 50},
    }

    response = client.put(f"/api/notifications/config/{config_id}", json=updated_config)

    assert response.status_code == 204

    updated_config = client.get(f"/api/notifications/config/{config_id}").json()

    assert updated_config["threshHold"]["cpu_usage"] == 50


def test_create_noticaition_unauthenticated(created_device):
    mocked_config = {
        "device_id": created_device["uuid"],
        "threshHold": {
            "watch_keys": ["cpu_usage"],
            "cpu_usage": 30,
        },
    }

    client.cookies.clear()
    with pytest.raises(HTTPException):
        response = client.post("/api/notifications/config", json=mocked_config)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
