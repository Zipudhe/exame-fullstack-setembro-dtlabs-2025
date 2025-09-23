import logging
from typing import Optional
from bson import ObjectId

from fastapi import APIRouter, HTTPException, Request, status

from src.schemas import CommonsDep

from .schemas import NotificationConfig, NotificationConfigOut, NotificationConfigUpdate
from .dependencies import NotificationsCollectionDep, NotificationsConfigCollectionDep
from ..devices.dependencies import DevicesCollectionDep

router = APIRouter(prefix="/notifications", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/config", response_model=Optional[list[NotificationConfigOut]])
async def get_notifications_config(
    request: Request, collection: NotificationsConfigCollectionDep
):
    user_id = request.state.user_id

    try:
        return collection.find({"user_id": user_id})
    except Exception as e:
        logger.error(f"Error fetching notification configs: {e}")
        raise HTTPException(500, detail="Failed to fetch notification configs") from e


@router.get("/config/{config_id}", response_model=Optional[NotificationConfigOut])
async def get_notification_config(
    config_id: str, request: Request, collection: NotificationsConfigCollectionDep
):
    user_id = request.state.user_id

    try:
        notificaiton_config = collection.find_one(
            {"user_id": user_id, "_id": ObjectId(config_id)}
        )
        return notificaiton_config
    except Exception as e:
        logger.error(f"Error fetching notification configs: {e}")
        raise HTTPException(500, detail="Failed to fetch notification configs") from e


@router.post("/config", status_code=status.HTTP_201_CREATED)
async def create_notifications_config(  # Subscribe to a notificaiton stream for device
    notificationConfig: NotificationConfig,
    request: Request,
    collection: NotificationsConfigCollectionDep,
):
    user_id = request.state.user_id
    new_config = {**notificationConfig.model_dump(), "user_id": user_id}

    try:
        collection.insert_one(new_config)
    except Exception as e:
        raise HTTPException(500, detail="Failed to create notification config") from e

    return


@router.put("/config/{notification_config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_notifications_config(
    notification_config_id: str,
    request: Request,
    collection: NotificationsConfigCollectionDep,
    notificationConfig: NotificationConfigUpdate,
):
    user_id = request.state.user_id

    try:
        collection.update_one(
            {"user_id": user_id, "_id": ObjectId(notification_config_id)},
            {"$set": notificationConfig.model_dump(exclude_unset=True)},
        )
    except Exception as e:
        logger.error(f"Error updating notification config: {e}")
        raise HTTPException(500, detail="Failed to update notification config") from e

    return


@router.delete(
    "/config/{notification_config_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notifications_config(
    notification_config_id: str,
    request: Request,
    collection: NotificationsConfigCollectionDep,
):
    user_id = request.state.user_id
    try:
        collection.delete_one(
            {"_id": ObjectId(notification_config_id), "user_id": user_id}
        )
    except Exception as e:
        logger.error(f"Error deleting notification config: {e}")
        raise HTTPException(500, detail="Failed to delete notification config") from e
    return


@router.get("/")
async def get_notifications(
    commons: CommonsDep, request: Request, collection: NotificationsCollectionDep
):
    return


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notifications(  # Notify user of event if it matches notification config
    request: Request, collection: NotificationsCollectionDep
):
    return


@router.put(
    "/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT
)  # Soft delete mark notification as read
async def mark_notification_as_read(
    notification_id: str,
    request: Request,
    notification_collection: NotificationsCollectionDep,
    device_collection: DevicesCollectionDep,
):
    user_id = request.state.user_id
    notificaiton = notification_collection.find_one({"_id": notification_id})
    if not notificaiton:
        raise HTTPException(status_code=404, detail="Notification not found")

    device = device_collection.find_one(
        {"_id": notificaiton["device_id"], "user_id": user_id}
    )

    if not device:
        raise HTTPException(
            status_code=401, detail="User not allowed to change notification"
        )

    try:
        device.update({"read": True})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to mark notification as read"
        ) from e

    return
