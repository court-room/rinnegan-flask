import datetime
import json
import logging
import os

from boto3 import client
from tweepy import API
from tweepy import AppAuthHandler
from tweepy import Cursor

from app import factory


log_format_string = "%(asctime)s PID- %(process)d %(levelname)s %(pathname)s %(funcName)s %(lineno)d %(message)s"  # noqa: E501

logging.basicConfig(level=logging.INFO, format=log_format_string)
logger = logging.getLogger(__name__)

app = factory.create_app(os.getenv("FLASK_ENV"))
app.app_context().push()


class AWSObjectStorageClient:
    def __init__(self):
        self.bucket = "rinnegan-data"
        self.client = client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def upload(self, local_file_path):
        s3_file_path = f"keywords-data/{local_file_path.split('/')[-1]}"

        self.client.upload_file(local_file_path, self.bucket, s3_file_path)


storage_clients = {"aws": AWSObjectStorageClient()}


def process_tweets(client, keyword, local_file_path):
    now = datetime.datetime.today() - datetime.timedelta(days=1)
    until = now.strftime("%Y-%m-%d")

    count = 0
    tweets = []

    for tweet in Cursor(
        client.search, q=keyword, lang="en", until=until
    ).items(1000):
        count += 1
        tweets.append(tweet._json)

        if count == 100:
            count = 0

            with open(local_file_path, "a") as fp:
                json.dump(tweets, fp)

            tweets = []

    with open(local_file_path, "a") as fp:
        json.dump(tweets, fp)


def push_to_object_storage(local_file_path):
    cloud_vendor = app.config.get("CLOUD_VENDOR")
    storage_client = storage_clients[cloud_vendor]

    storage_client.upload(local_file_path)


def start_analysis(keyword, request_id):
    """
    Adds a keyword to the queue for the worker to process

    :param: keyword
        keyword to find sentiment for
    """
    logger.info(f"Starting {keyword}")

    auth_wallet = AppAuthHandler(
        app.config.get("TWITTER_CONSUMER_KEY"),
        app.config.get("TWITTER_CONSUMER_SECRET"),
    )

    client = API(auth_wallet)

    local_file_path = f"/tmp/worker-data/{keyword}-{request_id}.json"

    process_tweets(client, keyword, local_file_path)

    push_to_object_storage(local_file_path)

    logger.info(f"Ending {keyword}")
