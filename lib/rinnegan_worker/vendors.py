import abc

from boto3 import client


class BaseClient(abc.ABC):
    def __init__(self):
        self.config = None

    @abc.abstractmethod
    def upload(self, local_file_path):
        pass


class AWSS3Client(BaseClient):
    def __init__(self):
        super().__init__()
        self.client = client(
            "s3",
            aws_access_key_id=self.config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=self.config.get("AWS_SECRET_ACCESS_KEY"),
        )

    def upload(self, local_file_path):
        remote_file_path = f"keywords-data/{local_file_path.split('/')[-1]}"

        self.client.upload_file(
            local_file_path, self.config.get("S3_BUCKET"), remote_file_path
        )


class AzureObjectStorageClient(BaseClient):
    def upload(self, local_file_path):
        pass


client_map = {"aws": AWSS3Client(), "azure": AzureObjectStorageClient()}
