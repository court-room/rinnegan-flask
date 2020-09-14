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
            return os.getenv(secret_file_path)


class TwitterConfig(BaseConfig):
    TWITTER_CONSUMER_KEY = BaseConfig.read_secrets(
        os.getenv("TWITTER_CONSUMER_KEY_FILE")
    )
    TWITTER_CONSUMER_SECRET = BaseConfig.read_secrets(
        os.getenv("TWITTER_CONSUMER_SECRET_FILE")
    )
    TWITTER_POST_LIMITS = int(
        BaseConfig.read_secrets(os.getenv("TWITTER_POST_LIMITS_FILE"))
    )
    TWITTER_POST_SCHEMA = ["text"]


class AWSConfig(BaseConfig):
    AWS_ACCESS_KEY_ID = BaseConfig.read_secrets(
        os.getenv("AWS_ACCESS_KEY_ID_FILE")
    )
    AWS_SECRET_ACCESS_KEY = BaseConfig.read_secrets(
        os.getenv("AWS_SECRET_ACCESS_KEY_FILE")
    )
    S3_BUCKET = BaseConfig.read_secrets(os.getenv("S3_BUCKET_FILE"))


class NLPModelConfig(BaseConfig):
    MONKEYLEARN_API_TOKEN = BaseConfig.read_secrets(
        os.getenv("MONKEYLEARN_API_TOKEN_FILE")
    )
    MONKEYLEARN_MODEL_ID = BaseConfig.read_secrets(
        os.getenv("MONKEYLEARN_MODEL_ID_FILE")
    )
    FLASK_ENV = os.getenv("FLASK_ENV")


class MongoDBClient(BaseConfig):
    MONGO_URI = BaseConfig.read_secrets(os.getenv("MONGO_URI_FILE"))
    MONGO_AUTH_SOURCE = BaseConfig.read_secrets(
        os.getenv("MONGO_AUTH_SOURCE_FILE")
    )
    MONGO_DATABASE = BaseConfig.read_secrets(os.getenv("MONGO_DATABASE_FILE"))
    MONGO_MODEL_COLLECTION = BaseConfig.read_secrets(
        os.getenv("MONGO_MODEL_COLLECTION_FILE")
    )


config_map = {
    "twitter": TwitterConfig,
    "aws": AWSConfig,
    "monkeylearn": NLPModelConfig,
    "mongo": MongoDBClient,
}
