import os
from logging.config import fileConfig


def setup_logger():
    config_path = os.path.join(os.path.dirname(__file__), "..", "logging.conf")

    fileConfig(os.path.abspath(config_path), disable_existing_loggers=False)
