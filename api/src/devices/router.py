import logging

from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import ServerSelectionTimeoutError

from src.websocket.stream import acknowledge_message

from src.devices.dependencies import (
    DevicesCollectionDep,
    DevicesQueryParamsDep,
)
from src.devices.services import DeviceEngine

from .schemas import (
    DeviceCreated,
    DeviceForm,
    DeviceDetails,
    HearBeat,
    DeviceUpdate,
    SummaryList,
)

router = APIRouter(prefix="/devices", tags=["devices"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=SummaryList)
async def get_devices(
    request: Request, service: DeviceEngine, commons: DevicesQueryParamsDep
):
    user_id = request.state.user_id
    try:
        pipeline = [
            {"$skip": commons["skip"]},
            {"$limit": commons["limit"]},
            {
                "$match": {"user_id": user_id, **commons["q"]},
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "name": 1,
                    "location": 1,
                    "sn": 1,
                    "description": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "status": {
                        "$arrayElemAt": ["$status", 0],
                    },
                }
            },
        ]
        result = service.find_all(query=pipeline)
        return SummaryList(data=result)
    except ServerSelectionTimeoutError as db_err:
        logger.error(f"Database connection error: {db_err}")
        raise HTTPException(status_code=503, detail="Database connection error")
    except Exception as e:
        logger.error(f"Error retrieving devices: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve devices")


@router.get("/{device_id}", response_model=DeviceDetails)
async def get_device(
    commons: DevicesQueryParamsDep,
    request: Request,
    device_id: str,
    service: DeviceEngine,
):
    user_id = request.state.user_id
    pipeline = [
        {
            "$match": {"id": device_id, "user_id": user_id, **commons["q"]},
        },
        {
            "$project": {
                "_id": 0,
                "id": 1,
                "name": 1,
                "location": 1,
                "sn": 1,
                "description": 1,
                "created_at": 1,
                "updated_at": 1,
                "status": {
                    "$slice": [
                        {
                            "$sortArray": {
                                "input": "$status",
                                "sortBy": {"created_at": -1},
                            }
                        },
                        commons["skip"],
                        commons["limit"],
                    ],
                },
            }
        },
    ]

    try:
        device = service.find_one(pipeline)
    except Exception as e:
        logger.error(f"Error retrieving device: {e}")
        raise HTTPException(500, "Failed to get device") from e

    logger.info(f"device: {device}")
    return device


@router.get("/{device_id}/status", response_model=list[HearBeat])
async def get_device_status(
    device_id: str,
    request: Request,
    devices_collection: DevicesCollectionDep,
    commons: DevicesQueryParamsDep,
):
    user_id = request.state.user_id

    filter_conditions = []
    query = commons["q"]

    logger.info(f"commons: {commons}")

    if "start_date" in query:
        filter_conditions.append(query["start_date"])

    if "end_date" in query:
        filter_conditions.append(query["end_date"])

    if filter_conditions:
        filter_cond = (
            {"$and": filter_conditions}
            if len(filter_conditions) > 1
            else filter_conditions[0]
        )
    else:
        filter_cond = True

    pipeline = [
        {
            "$match": {"id": device_id, "user_id": user_id},
        },
        {
            "$addFields": {
                "filtered_status": {
                    "$filter": {
                        "input": "$status",
                        "as": "item",
                        "cond": filter_cond,
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "status": {
                    "$slice": [
                        {
                            "$sortArray": {
                                "input": "$filtered_status",
                                "sortBy": {"created_at": -1},
                            }
                        },
                        commons["skip"],
                        commons["limit"],
                    ],
                },
            }
        },
    ]

    try:
        statuses = devices_collection.aggregate(pipeline)  # Revisar schema de saida

        if not statuses:
            return []

        status_list = statuses.to_list()[0].get("status")
        return status_list

    except Exception as e:
        logger.error(f"Error retrieving device status: {e}")
        raise HTTPException(500, "Failed to get device status") from e


@router.post("/{device_id}/status", status_code=status.HTTP_201_CREATED)
async def create_device_status(
    device_id: str,
    device_status: HearBeat,
    devices_collection: DevicesCollectionDep,
):
    new_status = device_status.model_dump()

    try:
        devices_collection.update_one(
            {"id": device_id},
            {"$push": {"status": {"$each": [new_status], "$position": 0}}},
        )

    except Exception as e:
        logger.error(f"Error creating device status: {e}")
        raise HTTPException(
            status_code=500, detail="Unable to create device status"
        ) from e

    return


@router.post("/ack")
async def ack_device_notification(request: Request, message_id: str):
    user_id = request.state.user_id
    await acknowledge_message(user_id, message_id)
    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeviceCreated)
async def create_device(
    device: DeviceForm,
    request: Request,
    service: DeviceEngine,
):
    user_id = request.state.user_id

    try:
        created_device_id = service.create(device, user_id)
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail="Unable to create device") from e

    return DeviceCreated(id=created_device_id)


@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(
    device_id: str,
    request: Request,
    service: DeviceEngine,
):
    user_id = request.state.user_id
    try:
        service.delete(device_id, user_id)
    except Exception as e:
        logger.error(f"Error deleting device: {device_id}\n detail: {e}")
        raise HTTPException(status_code=400, detail="Unable to delete device") from e
    return


@router.put("/{device_id}", status_code=status.HTTP_200_OK)
async def update_device(
    device_id: str,
    device: DeviceUpdate,
    collection: DevicesCollectionDep,
    request: Request,
):
    user_id = request.state.user_id
    update_values = device.model_dump(exclude_unset=True, exclude_none=True)
    filter = {"user_id": user_id, "id": device_id}

    try:
        collection.update_one(filter, {"$set": update_values})
    except Exception as e:
        logger.error(f"Error updating device: {device_id}\n detail: {e}")
        raise HTTPException(status_code=400, detail="Unable to update device") from e

    return
