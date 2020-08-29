import logging
import os

from app import factory


log_format_string = "%(asctime)s PID- %(process)d %(levelname)s %(pathname)s %(funcName)s %(lineno)d %(message)s"  # noqa: E501

logging.basicConfig(level=logging.INFO, format=log_format_string)
app = factory.create_app(os.getenv("FLASK_ENV"))
