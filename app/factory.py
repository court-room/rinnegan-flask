from flask import abort
from flask import Flask
from flask import request

from app.config import cfg_map


def create_app(environemnt, celery):
    """
    App factory for the server.

    Instantiates a Flask object.
    Configures the app according to the environment.
    Initializes the extensions.
    Adds the middleware to check headers.
    Returns the app instance.

    :param: environment
        Environemnt to configure the server to
    :returns:
    """
    app = Flask(__name__)
    app.config.from_object(cfg_map[environemnt])

    from app import bcrypt
    from app import celery
    from app import cors
    from app import db
    from app import migrate

    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    init_celery(celery, app)

    from app.api import api

    api.init_app(app)

    from app.api.auth.models import Token  # noqa: F401
    from app.api.sentiment.models import Sentiment  # noqa: F401
    from app.api.users.models import User  # noqa: F401

    @app.before_request
    def check_headers():
        if (
            "swagger" not in request.path
            and "admin" not in request.path
            and request.method != "OPTIONS"
        ):
            accepts = request.headers.get("Accept")
            if not accepts or accepts != "application/json":
                abort(415, "Only content type supported is application/json")
            if request.method in ["POST", "PUT"]:
                content_type = request.headers.get("Content-Type")
                if not content_type or content_type != "application/json":
                    abort(
                        415,
                        "POST/PUT requests should define Content-Type header",
                    )

    return app


def init_celery(celery, app):
    """
    Utility function to initialize the celery app,
    to use the flask app settings.

    :param: celery
        Instance of celery app to initialize
    :param: app
        Instance of flask app to add configs from
    """
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
