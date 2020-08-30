import abc

from boto3 import client

from lib.rinnegan_worker import config


cfg = config.Config()


class BaseClient(abc.ABC):
    @abc.abstractmethod
    def upload(local_file_path):
        pass


class AWSS3Client(BaseClient):
    def __init__(self):
        self.client = client(
            "s3",
            aws_access_key_id=cfg.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=cfg.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket = cfg.get("S3_BUCKET")

    def upload(self, local_file_path):
        remote_file_path = f"keywords-data/{local_file_path.split('/')[-1]}"

        self.client.upload_file(local_file_path, self.bucket, remote_file_path)


class AzureObjectStorageClient(BaseClient):
    def fetch_data(self, local_file_path):
        pass


client_map = {"aws": AWSS3Client(), "azure": AzureObjectStorageClient()}
