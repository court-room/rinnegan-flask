import logging
import logging.config
import os

import yaml

from app import celery
from app import factory


def setup_logging():
    """
    Function to setup logging.

    Reads the configuration from a .yml file.
    Initialises the logger with thatconfiguration.
    Installs coloredlogs to display logs in color format
    """
    try:
        with open("/usr/src/app/logging.yml", "r") as fp:
            config_dict = yaml.safe_load(fp.read())
            logging.config.dictConfig(config_dict)
    except yaml.constructor.ConstructorError as e:
        print(e)
        print("YML file for configuring the logger is invalid")
    except IOError as e:
        print(e)
        print("Unable to read config file")
    else:
        logging.info("Logging setup finished successfully")


setup_logging()
app = factory.create_app(os.getenv("FLASK_ENV"), celery=celery)
