import abc

from pymongo import MongoClient


# import json


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.config = config_obj
        self.data = None

    @abc.abstractmethod
    def start_streaming(self, keyword, response):
        pass


class MongoDBClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)
        host = self.config.MONGO_HOST
        port = self.config.MONGO_PORT
        username = self.config.MONGO_USER
        password=self.config.MONGO_PASSWORD
        database = self.config.MONGO_DATABASE
        connection_string = f"mongodb://{username}:{password}@{host}:{port}"
        self.client = MongoClient(connection_string)
        self.db = self.client[database]
        self.collection = self.db[self.config.MONGO_MODEL_COLLECTION]

    def start_streaming(self, keyword, responses):
        self.data = []

        for response in responses:
            temp = response
            temp["text"] = temp["text"].encode("ascii", "ignore").decode()
            for obj in temp["classifications"]:
                del obj["tag_id"]
            del temp["external_id"]
            self.data.append(temp)

        self.collection.insert_many(self.data)
        self.data = None


client_map = {"mongo": MongoDBClient}
