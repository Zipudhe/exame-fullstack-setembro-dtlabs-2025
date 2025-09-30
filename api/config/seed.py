import random
import sys

from src.devices.schemas import Device, DeviceStatusInput
from src.notifications.schemas import NotificationConfig, ThreshHoldConfig
from src.users.utils import Hasher
from src.users.schemas import UserIn
from src.notifications.dependencies import get_notifications_config_collection
from src.users.dependencies import get_user_collection
from src.devices.dependencies import get_devices_collection
from src.database import get_database
from .device_helper import create_device

from faker import Faker

QTD_DEVICES = 1
QTD_NOTIFICATION_CONFIG = 2

faker = Faker()
db = get_database()

notification_collection = get_notifications_config_collection(db)
users_collection = get_user_collection(db)
devices_collection = get_devices_collection(db)


def drop_collections():
    collections = db.list_collection_names()
    for coll in collections:
        db.drop_collection(coll)


if __name__ == "__main__":
    print(f"sys arg: {sys.argv}")
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("RESETING DATABASE")
        drop_collections()

    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        print("DROPPING DATABASE")
        drop_collections()
        exit()

    email = faker.email()
    password = faker.password(length=8, digits=True, special_chars=True)
    user = UserIn(
        email=email, username=faker.user_name(), password=password
    ).model_dump()
    hashed_password = Hasher.get_password_hash(user["password"])
    user["password"] = hashed_password

    print(f"reference user credentias: {email}:{password}")
    user_id = user["id"]

    users_collection.insert_one(user)

    if not user_id:
        print("Failed to create user")
        exit()

    print(f"------- seeding {QTD_DEVICES} devices for user...------- ")
    devices = []
    for _ in range(QTD_DEVICES):
        device = Device(
            name=faker.word(),
            location=faker.city(),
            sn=faker.unique.bothify(text="############"),
            description=faker.sentence(),
        ).model_dump()
        device["user_id"] = user_id
        print("created device:", device["id"])
        create_device(
            endpoint=f"/api/devices/{device['id']}/status",
            device_id=device["id"],
            user_id=user_id,
            interval=10,
        )

        status = []
        for _ in range(random.randint(1, 5)):
            device_status = DeviceStatusInput(
                cpu_usage=faker.random_int(min=0, max=100),
                ram_usage=faker.random_int(min=0, max=100),
                free_disk=faker.random_int(min=0, max=100),
                temperature=faker.random_int(min=20, max=90),
                latency=faker.random_int(min=0, max=500),
                connectivity=faker.boolean(chance_of_getting_true=90),
                boot_date=faker.date_this_decade().isoformat(),
            ).model_dump()

            status.append(device_status)

        device["status"] = status
        devices.append(device)

    print("-------------------------")

    print(f"seeding {QTD_NOTIFICATION_CONFIG} notification configs...")
    notification_list = []
    for _ in range(QTD_NOTIFICATION_CONFIG):
        threshHold = ThreshHoldConfig(
            cpu_usage=faker.random_int(min=50, max=100),
            ram_usage=faker.random_int(min=50, max=100),
            free_disk=faker.random_int(min=0, max=50),
            temperature=faker.random_int(min=60, max=90),
            latency=faker.random_int(min=200, max=500),
            watch_keys=faker.words(
                nb=random.randint(1, 5),
                unique=True,
                ext_word_list=[
                    "cpu_usage",
                    "ram_usage",
                    "free_disk",
                    "temperature",
                    "latency",
                ],
            ),
        )

        notification_config = NotificationConfig(
            user_id=user_id,
            threshHold=threshHold,
        ).model_dump()
        notification_list.append(notification_config)

    if len(devices) != len(set(id(d) for d in devices)):
        print("⚠️ DEBUG: The 'devices' list contains duplicate object references!")

    if len(notification_list) != len(set(id(n) for n in notification_list)):
        print("⚠️ DEBUG: The 'notification_list' contains duplicate object references!")

    with db.client.start_session() as session:
        devices_collection.insert_many(devices, session=session)
        notification_collection.insert_many(notification_list, session=session)
    print("finished seeding database")
