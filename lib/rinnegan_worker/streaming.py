import abc
import json

from pymongo import MongoClient


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.config = config_obj

    @abc.abstractmethod
    def start_streaming(self, keyword, data_file_path):
        pass


class MongoDBClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)

        self.client = MongoClient(self.config.MONGO_URI)

    def start_streaming(self, keyword, data_file_path):
        with open(data_file_path, "r") as fp:

            data = []
            for index, line in enumerate(fp.readlines()):
                if index == 500:
                    # Push t
                    pass



client_map = {"mongo": MongoDBClient}
