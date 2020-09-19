import abc

from boto3 import client


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.config = config_obj

    @abc.abstractmethod
    def upload(self, local_file_path):
        pass


class AWSS3Client(BaseClient):
    def __init__(self, config):
        super().__init__(config)
        self.client = client(
            "s3",
            aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        )

    def upload(self, local_file_path):
        remote_file_path = f"keyword-data/{local_file_path.split('/')[-1]}"

        self.client.upload_file(
            local_file_path, self.config.S3_BUCKET, remote_file_path
        )


client_map = {"aws": AWSS3Client}
