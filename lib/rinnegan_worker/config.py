import os


class BaseConfig:
    @staticmethod
    def read_secrets(secret_file_path):
        """
        Utility method to fetch secrets depending upon the environment.
        First an attempt is made to read the secret from the file
        defined in the env variable.
        If the file does not exist then the value read is returned.

        :param: secret_file_path
            Path to file or the secret
        :returns:
            Secret stored in the environment or the file
        """
        try:
            with open(secret_file_path, "r") as fp:
                secret = fp.readline().strip()
            return secret
        except (FileNotFoundError, TypeError):
            return secret_file_path


class TwitterConfig(BaseConfig):
    # TWITTER_CONSUMER_KEY = BaseConfig.read_secrets("TWITTER_CONSUMER_KEY")
    # TWITTER_CONSUMER_SECRET = BaseConfig.read_secrets(
    #     "TWITTER_CONSUMER_SECRET"
    # )
    TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")


class AWSConfig(BaseConfig):
    # AWS_ACCESS_KEY_ID = BaseConfig.read_secrets("AWS_ACCESS_KEY_ID")
    # AWS_SECRET_ACCESS_KEY = BaseConfig.read_secrets("AWS_SECRET_ACCESS_KEY")
    # S3_BUCKET = BaseConfig.read_secrets("S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = "rinnegan-data"


config_map = {"twitter": TwitterConfig, "aws": AWSConfig}
