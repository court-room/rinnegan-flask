import os


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


class BaseConfig:
    TESTING = True
    SECRET_KEY = read_secrets(os.getenv("SECRET_KEY_FILE"))
    JSON_SORT_KEYS = True
    HEALTHCHECK_FILE_PATH = "/usr/src/app/heartbeat.txt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = read_secrets(os.getenv("DATABASE_URL_FILE"))
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900
    REFRESH_TOKEN_EXPIRATION = 2592000
    JWT_ENCODE_ALGORITHM = "HS256"
    SENTIMENT_QUOTA_LIMIT = 5
    REDIS_URL = read_secrets(os.getenv("REDIS_URL_FILE"))
    REDIS_QUEUE_NAME = "rinnegan"
    CLOUD_VENDOR = read_secrets(os.getenv("CLOUD_VENDOR"))
    AWS_ACCESS_KEY_ID = read_secrets(os.getenv("AWS_ACCESS_KEY_ID"))
    AWS_SECRET_ACCESS_KEY = read_secrets(os.getenv("AWS_SECRET_ACCESS_KEY"))
    MONGO_URI = read_secrets(os.getenv("MONGO_URI_FILE"))
    MONGO_AUTH_SOURCE = read_secrets(os.getenv("MONGO_AUTH_SOURCE_FILE"))
    MONGO_DATABASE = read_secrets(os.getenv("MONGO_DATABASE_FILE"))
    MONGO_MODEL_COLLECTION = read_secrets(
        os.getenv("MONGO_MODEL_COLLECTION_FILE")
    )
    POSTS_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 4
    JWT_ENCODE_ALGORITHM = "HS384"
    POSTS_PER_PAGE = 2


class TestingConfig(BaseConfig):
    REDIS_URL = "placeholder"
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL_FILE")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3
    REDIS_URL = "redis://"
    TWITTER_CONSUMER_KEY = "dummy"
    TWITTER_CONSUMER_SECRET = "dummy"
    MONGO_URI = read_secrets(os.getenv("MONGO_URI_FILE"))
    MONGO_AUTH_SOURCE = read_secrets(os.getenv("MONGO_AUTH_SOURCE_FILE"))


class ProductionConfig(BaseConfig):
    TESTING = False
    JWT_ENCODE_ALGORITHM = "HS512"


cfg_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
