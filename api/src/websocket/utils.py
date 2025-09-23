from config.env_vars import get_enviroment


def get_stream_key(user_id: str) -> str:
    env = get_enviroment()
    stream_sufix = "notification"
    return f"{env}:{user_id}:{stream_sufix}"


def get_consumer_group() -> str:
    env = get_enviroment()
    group_sufix = "notification_group"
    return f"{env}:{group_sufix}"
