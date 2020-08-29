import logging
import os

from tweepy import AppAuthHandler

from app import factory


log_format_string = "%(asctime)s PID- %(process)d %(levelname)s %(pathname)s %(funcName)s %(lineno)d %(message)s"  # noqa: E501

logging.basicConfig(level=logging.INFO, format=log_format_string)
logger = logging.getLogger(__name__)

app = factory.create_app(os.getenv("FLASK_ENV"))
app.app_context().push()



def start_analysis(keyword):
    """
    Adds a keyword to the queue for the worker to process

    :param: keyword
        keyword to find sentiment for
    """
    # with app.app_context():
    logger.info(f"Starting {keyword}")

    auth_wallet = AppAuthHandler(app.config.get("TWITTER_CONSUMER_KEY"), app.config.get("TWITTER_CONSUMER_SECRET"))

    logger.info(f"Ending {keyword}")
