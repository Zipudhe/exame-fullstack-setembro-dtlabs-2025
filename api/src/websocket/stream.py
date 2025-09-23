import asyncio
import logging

from src.database import get_async_redis_storage

from .utils import get_consumer_group, get_stream_key

logger = logging.getLogger(__name__)

GROUP_NAME = get_consumer_group()
MAX_STREAM_LENGTH = 1000
XREAD_TIMEOUT = 5000
XREAD_COUNT = 1

redis_client = get_async_redis_storage()


async def publish_to_stream(user_id: str, message: str):
    stream_key = get_stream_key(user_id)
    payload = {"message": message}

    try:
        msg_id = await redis_client.xadd(
            stream_key, payload, maxlen=MAX_STREAM_LENGTH, approximate=True
        )
    except Exception as e:
        logger.error(f"Error publishing to stream {stream_key}: {e}")


async def create_consumer_group(user_id: str):
    stream_key = get_stream_key(user_id)

    try:
        await redis_client.xgroup_create(stream_key, GROUP_NAME, id="$", mkstream=True)
    except Exception as e:
        if "BUSYGROUP" in str(e):
            logger.info(f"Consumer group {GROUP_NAME} already exists for {stream_key}")
        else:
            logger.error(f"Error creating consumer group for {stream_key}: {e}")


async def get_pending_messages(user_id: str):
    stream_key = get_stream_key(user_id)
    consumer_name = user_id

    try:
        pending_messages = await redis_client.xreadgroup(
            GROUP_NAME, consumer_name, {stream_key: "0"}, count=XREAD_COUNT, block=0
        )
        if pending_messages:
            for _stream, messages in pending_messages:
                logger.info(f"Pending messages for {user_id}: {messages}")

        return pending_messages
    except Exception as e:
        logger.error(f"Error reading pending messages from {stream_key}: {e}")
        return []


async def listen_to_stream(user_id: str, websocket):
    stream_key = get_stream_key(user_id)
    consumer_name = user_id

    while True:
        try:
            new_message = await redis_client.xreadgroup(
                GROUP_NAME,
                consumer_name,
                {stream_key: ">"},
                count=XREAD_COUNT,
                block=XREAD_TIMEOUT,
            )

            if new_message:
                for _stream, messages in new_message:
                    for message_id, message_data in messages:
                        message = message_data.get(b"message", b"").decode("utf-8")
                        logger.info(f"Sending message to {user_id}: {message}")
                        await websocket.send_text(message)
            else:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error listening to stream {stream_key}: {e}")
            await asyncio.sleep(1)


async def acknowledge_message(user_id: str, message_id: str):
    stream_key = get_stream_key(user_id)
    try:
        if message_id:
            await redis_client.xack(stream_key, GROUP_NAME, message_id)
    except Exception as e:
        logger.error(f"Error acknowledging message {message_id} in {stream_key}: {e}")
