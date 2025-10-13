from src.database import get_database
from src.notifications.dependencies import get_notifications_collection


db = get_database()


def check_notification_config(user_id: str):
    notifications_config_collection = get_notifications_collection(db)
