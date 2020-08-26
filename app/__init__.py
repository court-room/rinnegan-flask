from celery import Celery
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
migrate = Migrate()


def make_celery(app_name=__name__):
    """
    Utility function to create a celery instance
    This instance will be used througout the app

    :params: app_name
        Name of the app to register
    :returns:
        Instance of celery
    """
    backend = "redis://:rinnegan@redis:6379/0"
    broker = backend.replace("0", "1")

    return Celery(
        app_name,
        backend=backend,
        broker=broker,
        include=["app.api.sentiment.tasks"],
    )


celery = make_celery(app_name=__name__)
