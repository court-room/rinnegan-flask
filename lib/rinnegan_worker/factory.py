import abc

from lib.rinnegan_worker.config import config_map
from lib.rinnegan_worker.sources import client_map as source_client_map
from lib.rinnegan_worker.vendors import client_map as vendor_client_map


class BaseFactory(abc.ABC):
    @abc.abstractstaticmethod
    def build_client(source):
        pass


class SourceClientFactory(BaseFactory):
    @staticmethod
    def build_client(source):
        client = source_client_map.get(source, None)
        if not client:
            error = f"""
            Following source:- {source} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return client(config_map[source]())


class StorageVendorClientFactory(BaseFactory):
    @staticmethod
    def build_client(vendor):
        client = vendor_client_map.get(vendor, None)
        if not client:
            error = f"""
            Following vendor:- {vendor} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return client(config_map[vendor]())
