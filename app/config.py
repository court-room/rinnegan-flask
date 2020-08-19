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
    except FileNotFoundError:
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


class DevelopmentConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 4
    JWT_ENCODE_ALGORITHM = "HS384"


class TestingConfig(BaseConfig):
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL_FILE")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    TESTING = False
    JWT_ENCODE_ALGORITHM = "HS512"


cfg_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
