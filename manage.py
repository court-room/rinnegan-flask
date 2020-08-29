import logging
import os

from app import factory


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s PID- %(process)d %(levelname)s %(pathname)s %(funcName)s %(lineno)d %(message)s",
)
app = factory.create_app(os.getenv("FLASK_ENV"))
