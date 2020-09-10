import abc

from pymongo import MongoClient


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
        self.client = MongoClient(
            self.config.MONGO_URI, authSource=self.config.MONGO_AUTH_SOURCE
        )
        self.db = self.client[self.config.MONGO_DATABASE]
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
