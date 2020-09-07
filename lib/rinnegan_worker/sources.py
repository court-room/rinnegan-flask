import abc
import datetime
import json

from tweepy import API
from tweepy import AppAuthHandler
from tweepy import Cursor


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.count = 0
        self.data = []
        self.config = config_obj

    @abc.abstractmethod
    def fetch_data(self, keyword, data_file_path):
        pass

    def write_to_json(self, data_file_path):
        with open(data_file_path, "a") as fp:
            for data in self.data:
                try:
                    output = self._compactify(data)
                    fp.write(f"{output}\n")
                except json.decoder.JSONDecodeError:
                    fp.write("Error processign data")


class TwitterClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)
        auth_wallet = AppAuthHandler(
            self.config.TWITTER_CONSUMER_KEY,
            self.config.TWITTER_CONSUMER_SECRET,
        )
        self.client = API(auth_wallet)

    def _compactify(self, record):
        result = {}

        for key in self.config.TWITTER_POST_SCHEMA:
            if key in record:
                result[key] = record[key]

        return result

    def write_to_json(self, data_file_path):
        with open(data_file_path, "a") as fp:

            for data in self.data:
                try:
                    output = self._compactify(data)
                    fp.write(f"{output}\n")
                except json.decoder.JSONDecodeError:
                    pass

        self.count = 0
        self.data = []

    def fetch_data(self, keyword, data_file_path):
        now = datetime.datetime.today() - datetime.timedelta(days=1)
        until = now.strftime("%Y-%m-%d")

        for tweet in Cursor(
            self.client.search, q=keyword, lang="en", until=until
        ).items(self.config.TWITTER_POST_LIMITS):
            self.count += 1

            # skipcq: PYL-W0212
            self.data.append(tweet._json)

            if self.count == 100:
                self.write_to_json(data_file_path)

        self.write_to_json(data_file_path)


client_map = {"twitter": TwitterClient}
