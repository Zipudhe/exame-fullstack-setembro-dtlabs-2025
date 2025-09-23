import logging

from config.env_vars import get_database_credentials, get_database_host, get_redis_host
from pymongo import MongoClient
from pymongo.database import Database
from redis import Redis
from redis import asyncio

logger = logging.getLogger(__name__)


def get_db_client() -> MongoClient:
    (username, password) = get_database_credentials()
    host = get_database_host()
    connectionString = f"mongodb://{username}:{password}@{host}:27017"
    logger.debug(f"connectionString: {connectionString}")

    try:
        client = MongoClient(connectionString)
        return client
    except Exception as e:
        logger.error(f"Unable to connec to mongodb client due to:\n {e}")
        raise Exception("Unable to connect to mongodb client")


def get_database() -> Database:
    client = get_db_client()
    return Database(client, "iotDevices")


def check_client_connection():
    client = get_db_client()
    logger.debug(f"client: {client}")
    return client.admin.command("ping")


def get_redis_storage():
    host = get_redis_host()
    return Redis(host=host, port=6379, db=0, decode_responses=True)


def get_async_redis_storage():
    host = get_redis_host()
    return asyncio.Redis(host=host, port=6379, db=0, decode_responses=True)
