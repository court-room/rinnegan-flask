import logging

from flask_restx import Namespace
from flask_restx import Resource

from app.api.health.crud import get_health_status


logger = logging.getLogger(__name__)
health_namespace = Namespace("health")


class Health(Resource):
    @staticmethod
    @health_namespace.response(200, "Health check passing")
    @health_namespace.response(404, "Health check failed")
    def get():
        response = get_health_status()

        logger.info("Health check passing")
        return response, 200


health_namespace.add_resource(Health, "")
