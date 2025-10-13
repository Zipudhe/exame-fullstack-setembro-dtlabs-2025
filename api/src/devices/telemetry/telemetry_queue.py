import logging
from rq import Queue
from rq.repeat import Repeat
from src.database import get_redis_storage
from src.database import get_database
from src.devices.dependencies import get_devices_collection
from src.devices.utils import check_notification_config
from src.websocket.stream import publish_to_stream
from .telemetry_sim import collect_telemetry

logger = logging.getLogger(__name__)
redis_client = get_redis_storage()

telemetry_queue = Queue(connection=redis_client)
INTERVAL = 60


def add_device_job(device_info: tuple[str, str]):
    print(f"adding device: {device_info[0]}")
    telemetry_queue.enqueue(
        add_status, device_info[0], device_info[1], Repeat(times=1, interval=INTERVAL)
    )


db = get_database()
logger = logging.getLogger(__name__)


async def add_status(device_info: tuple[str, str]):
    device_id = device_info[0]
    user_id = device_info[1]

    devices_collection = get_devices_collection(db)
    status = collect_telemetry().model_dump()
    print(f"status: {status}")

    try:
        devices_collection.update_one(
            {"id": device_id},
            {"$push": {"status": {"$each": [status], "$position": 0}}},
        )
        matches_config = check_notification_config(user_id=user_id)

        if matches_config:
            await publish_to_stream(user_id, "matched config")

    except Exception as e:
        logger.error(f"Error creating device status: {e}")

    add_device_job(device_info)
