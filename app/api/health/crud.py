import json

from flask import current_app as app


def get_health_status():
    return {"health": "good"}
