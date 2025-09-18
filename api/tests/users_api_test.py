import logging

import pytest
from fastapi.testclient import TestClient
from pymongo.database import Database

from main import app
from src.database import get_database, get_db_client

client = TestClient(app)
logger = logging.getLogger(__name__)


def get_database_override():
    client = get_db_client()
    return Database(client, "test_database")


app.dependency_overrides[get_database] = get_database_override


@pytest.fixture(autouse=True)
def database_cleanup():
    yield

    print("TEARDOWN STARTED....\n")
    client = get_db_client()
    client.drop_database("test_database")
    print("TEARDOWN COMPLETE\n")


@pytest.fixture()
def created_user():
    user_credentials = {
        "username": "testuser",
        "password": "VerySecurepassword123",
    }

    response = client.post("/api/users", data=user_credentials)
    assert response.status_code == 201
    yield user_credentials


def test_create_valid_user():
    mocked_user = {
        "username": "testuser",
        "password": "VerySecurepassword123",
    }

    response = client.post("/api/users", data=mocked_user)

    assert response.status_code == 201
    user_id = response.json().get("id", "")

    assert not user_id == ""

    created_user_response = client.get(f"/api/users/{user_id}")

    db_user = created_user_response.json()

    assert db_user["id"] == user_id


def test_create_week_password_user():
    expected_message = "Value error, Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number."
    mocked_user = {
        "username": "testuser",
        "password": "Notsostrong",
    }

    response = client.post("/api/users", data=mocked_user)

    assert response.status_code == 422
    message = response.json()["detail"][0]["msg"]
    logger.info(f"message: {message}")
    assert message == expected_message


def test_login_user(created_user):
    response = client.post("/api/users/login", data=created_user)

    assert response.status_code == 200
    assert response.cookies.get("session_id", "") != ""
