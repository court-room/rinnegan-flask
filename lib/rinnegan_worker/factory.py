from lib.rinnegan_worker.sources import client_map as source_client_map
from lib.rinnegan_worker.vendors import client_map as vendor_client_map


class SourceClientFactory:
    def __init__(self, source):
        self.source = source
        self.client = source_client_map.get(source, None)

    def build_client(self):
        if not self.client:
            error = f"""
            Following source:- {self.source} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return self.client


class StorageVendorClientFactory:
    def __init__(self, vendor):
        self.vendor = vendor
        self.client = vendor_client_map.get(vendor, None)

    def build_client(self):
        if not self.client:
            error = f"""
            Following vendor:- {self.vendor} is not integrated with rinnegan
            """
            raise NotImplementedError(error)

        return self.client
