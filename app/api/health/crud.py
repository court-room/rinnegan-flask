import json

from flask import current_app as app


def get_health_status():
    try:
        with open(app.config["HEALTHCHECK_FILE_PATH"], "r") as fp:
            health = json.load(fp)
            return health
    except IOError:
        return {"health": "bad"}
