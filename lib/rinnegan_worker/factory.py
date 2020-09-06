import abc

from lib.rinnegan_worker.config import config_map
from lib.rinnegan_worker.models import client_map as model_client_map
from lib.rinnegan_worker.sources import client_map as source_client_map
from lib.rinnegan_worker.vendors import client_map as vendor_client_map


class BaseFactory(abc.ABC):
    @abc.abstractstaticmethod
    def build_client(client_type):
        pass


class SourceClientFactory(BaseFactory):
    @staticmethod
    def build_client(client_type):
        client = source_client_map.get(client_type, None)
        if not client:
            error = f"""
            Following source:- {client_type} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return client(config_map[client_type]())


class StorageVendorClientFactory(BaseFactory):
    @staticmethod
    def build_client(client_type):
        client = vendor_client_map.get(client_type, None)
        if not client:
            error = f"""
            Following vendor:- {client_type} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return client(config_map[client_type]())


class NLPModelClientFactory(BaseFactory):
    @staticmethod
    def build_client(client_type):
        client = model_client_map.get(client_type, None)
        if not client:
            error = f"""
            Following vendor:- {client_type} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return client(config_map[client_type]())
