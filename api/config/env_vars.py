import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_port():
    return int(os.getenv("PORT", "8000"))


def get_enviroment():
    return os.getenv("ENV", "development")


def get_allowed_hosts():
    white_list_string = os.getenv("WHITE_LIST", "")

    if not white_list_string:
        return list("*")

    return white_list_string.split(",")
