from flask_restx import fields
from flask_restx import Namespace

from app.api.auth.serializers import auth_namespace


users_namespace = Namespace("users")

user_readable = users_namespace.model(
    "Existing-User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

parser = auth_namespace.parser()
parser.add_argument("Authorization", location="headers", required=True)
parser.add_argument("page", location="args")
