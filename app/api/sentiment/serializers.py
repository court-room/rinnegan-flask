from flask_restx import fields
from flask_restx import Namespace

from app.api.auth.serializers import auth_namespace


sentiment_namespace = Namespace("sentiment")

sentiment_schema = sentiment_namespace.model(
    "Sentiment",
    {
        "job_id": fields.Integer(readOnly=True),
        "user_id": fields.Integer(required=True),
        "keyword": fields.String(required=True),
    },
)

update_sentiment_schema = sentiment_namespace.model(
    "Update Sentiment",
    {
        "id": fields.Integer(readOnly=True),
        "keyword": fields.String(required=True),
    },
)

sentiment_score_schema = sentiment_namespace.model(
    "Sentiment",
    {
        "sentiment_id": fields.String(readOnly=True),
        "score": fields.Float(required=True),
    },
)

parser = auth_namespace.parser()
parser.add_argument("Authorization", location="headers", required=True)
parser.add_argument("page", location="args")
