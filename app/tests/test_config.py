# Test development config
def test_development_config(test_app):
    test_app.config.from_object("app.config.DevelopmentConfig")
    config = test_app.config

    if not config["TESTING"]:
        raise AssertionError
    if not config["SECRET_KEY"]:
        raise AssertionError
    if not config["JSON_SORT_KEYS"]:
        raise AssertionError
    if config["SQLALCHEMY_TRACK_MODIFICATIONS"]:
        raise AssertionError
    if not config["SQLALCHEMY_DATABASE_URI"]:
        raise AssertionError
    if config["BCRYPT_LOG_ROUNDS"] != 4:
        raise AssertionError
    if test_app.config["ACCESS_TOKEN_EXPIRATION"] != 900:
        raise AssertionError
    if test_app.config["REFRESH_TOKEN_EXPIRATION"] != 2592000:
        raise AssertionError
    if test_app.config["JWT_ENCODE_ALGORITHM"] != "HS384":
        raise AssertionError


# Test testing config
def test_testing_config(test_app):
    test_app.config.from_object("app.config.TestingConfig")
    config = test_app.config

    if not config["TESTING"]:
        raise AssertionError
    if not config["SECRET_KEY"]:
        raise AssertionError
    if config["JSON_SORT_KEYS"]:
        raise AssertionError
    if config["SQLALCHEMY_TRACK_MODIFICATIONS"]:
        raise AssertionError
    if not config["SQLALCHEMY_DATABASE_URI"]:
        raise AssertionError
    if config["BCRYPT_LOG_ROUNDS"] != 4:
        raise AssertionError
    if test_app.config["ACCESS_TOKEN_EXPIRATION"] != 3:
        raise AssertionError
    if test_app.config["REFRESH_TOKEN_EXPIRATION"] != 3:
        raise AssertionError
    if test_app.config["JWT_ENCODE_ALGORITHM"] != "HS256":
        raise AssertionError


# Test production config
def test_production_config(test_app):
    test_app.config.from_object("app.config.ProductionConfig")
    config = test_app.config

    if config["TESTING"]:
        raise AssertionError
    if not config["SECRET_KEY"]:
        raise AssertionError
    if not config["JSON_SORT_KEYS"]:
        raise AssertionError
    if config["SQLALCHEMY_TRACK_MODIFICATIONS"]:
        raise AssertionError
    if not config["SQLALCHEMY_DATABASE_URI"]:
        raise AssertionError
    if config["BCRYPT_LOG_ROUNDS"] != 13:
        raise AssertionError
    if test_app.config["ACCESS_TOKEN_EXPIRATION"] != 900:
        raise AssertionError
    if test_app.config["REFRESH_TOKEN_EXPIRATION"] != 2592000:
        raise AssertionError
    if test_app.config["JWT_ENCODE_ALGORITHM"] != "HS512":
        raise AssertionError
