import logging
import asyncio
from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect, status

from src.websocket.stream import (
    create_consumer_group,
    get_pending_messages,
    listen_to_stream,
    publish_to_stream,
)
from .manager import manager

router = APIRouter(prefix="/ws", tags=["websocket"])

logger = logging.getLogger(__name__)


@router.websocket("/notification")
async def websocket_endpoint(websocket: WebSocket, request: Request):
    user_id = request.state.user_id

    await manager.connect(websocket, user_id)

    try:
        await create_consumer_group(user_id)

    except Exception:
        logger.error("Failed to create consumer group")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return

    try:
        pending_messages = await get_pending_messages(user_id)
        if pending_messages:
            logger.info(f"Sending pending messages to user {pending_messages}")
            for msg in pending_messages[0][1]:
                message = msg[1].get(b"message", b"").decode("utf-8")
                await websocket.send_text(message)

    except Exception as e:
        logger.error(f"Failed to read pending messages: {e}")

    listener_task = asyncio.create_task(listen_to_stream(user_id, websocket))

    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages.
            await publish_to_stream(user_id, f"[Echo] {data}")
    except WebSocketDisconnect as e:
        logger.info("WebSocket disconnected: %s", e)
    except Exception as e:
        logger.error("Unexpected error on WebSocket connection: %s", e)
    finally:
        await manager.disconnect(user_id, websocket)
        listener_task.cancel()
