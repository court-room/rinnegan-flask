import abc

from pymongo import MongoClient


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.config = config_obj

    @abc.abstractmethod
    def start_streaming(self, keyword, response):
        pass


class MongoDBClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)

        self.client = MongoClient(self.config.MONGO_URI)
        self._check_index_exists()
    
    def _check_index_exists(self):
        pass

    def start_streaming(self, keyword, response):
        pass


client_map = {"mongo": MongoDBClient}
