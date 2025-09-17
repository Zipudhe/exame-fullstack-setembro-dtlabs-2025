import logging
from pymongo import MongoClient
from config.env_vars import get_database_host, get_database_credentials

logger = logging.getLogger(__name__)


def get_client() -> MongoClient:
    (username, password) = get_database_credentials()
    host = get_database_host()
    connectionString = f"mongodb://{username}:{password}@{host}:27017"
    logger.info(f"mongo connectionString: {connectionString}")
    try:
        client = MongoClient(connectionString)
        return client
    except Exception as e:
        logger.error(f"Unable to connec to mongodb client due to:\n {e}")
        raise Exception("Unable to connect to mongodb client")


def check_client_connection():
    client = get_client()
    logger.debug(f"client: {client}")
    return client.admin.command("ping")
