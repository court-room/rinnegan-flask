import abc
import datetime
import json

from tweepy import API
from tweepy import AppAuthHandler
from tweepy import Cursor


class BaseClient(abc.ABC):
    def __init__(self):
        self.count = 0
        self.data = []
        self.config = None

    @abc.abstractmethod
    def fetch_data(self, keyword, request_id):
        pass

    def write_to_json(self, keyword, request_id):
        local_file_path = f"/tmp/worker-data/{keyword}-{request_id}"

        with open(local_file_path, "a") as fp:
            json.dump(self.data, fp)


class TwitterClient(BaseClient):
    def __init__(self):
        super().__init__()

        auth_wallet = AppAuthHandler(
            self.config.get("TWITTER_CONSUMER_KEY"),
            self.config.get("TWITTER_CONSUMER_SECRET"),
        )
        self.client = API(auth_wallet)

    def write_to_json(self, keyword, request_id):
        super().write_to_json(keyword=keyword, request_id=request_id)

        self.count = 0
        self.data = []

    def fetch_data(self, keyword, request_id):
        now = datetime.datetime.today() - datetime.timedelta(days=1)
        until = now.strftime("%Y-%m-%d")

        for tweet in Cursor(
            self.client.search, q=keyword, lang="en", until=until
        ).items(1000):
            self.count += 1
            self.data.append(tweet._json)

            if self.count == 100:
                self.write_to_json(keyword=keyword, request_id=request_id)

        self.write_to_json(keyword=keyword, request_id=request_id)


class FacebookClient(BaseClient):
    def fetch_data(self, keyword, request_id):
        pass


client_map = {"twitter": TwitterClient(), "facebook": FacebookClient()}
