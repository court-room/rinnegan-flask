import logging
import uuid

from flask import current_app
from flask import request
from flask_restx import Resource
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError

from app.api.auth.crud import get_user_id_by_token
from app.api.auth.serializers import parser
from app.api.sentiment.crud import add_sentiment
from app.api.sentiment.crud import get_all_sentiments
from app.api.sentiment.crud import get_sentiment_by_id
from app.api.sentiment.crud import is_user_sentiment_quota_exhausted
from app.api.sentiment.crud import remove_sentiment
from app.api.sentiment.crud import update_sentiment
from app.api.sentiment.serializers import sentiment_namespace
from app.api.sentiment.serializers import sentiment_schema
from app.api.sentiment.serializers import update_sentiment_schema
from app.api.users.crud import get_user_by_id


logger = logging.getLogger(__name__)


class SentimentList(Resource):
    @staticmethod
    # Use multiple expect blocks in swagger UI
    # @sentiment_namespace.expect(parser)
    @sentiment_namespace.expect(sentiment_schema, validate=True)
    @sentiment_namespace.response(201, "Successfully added the keyword")
    @sentiment_namespace.response(
        403, "Sorry.The provided user is not registered"
    )
    def post():
        request_data = request.get_json()
        keyword = request_data["keyword"]
        user_id = request_data["user_id"]
        response = {}

        user_exists = get_user_by_id(user_id)
        if not user_exists:
            logger.info(f"User with id {user_id} does not exists")
            response["message"] = "Sorry.The provided user is not registered"
            return response, 403

        if not is_user_sentiment_quota_exhausted(user_id):
            request_id = uuid.uuid4().hex

            params = {
                "keyword": {"data": keyword},
                "meta": {"request_id": request_id, "model": "monkeylearn"},
                "source": {"data": "twitter"},
                "object_storage_vendor": {"data": "aws"},
                "streaming": {"data": "mongo"},
            }

            job = current_app.task_queue.enqueue(
                "lib.rinnegan_worker.handlers.start_analysis",
                params,
                job_timeout="5h",
            )

            add_sentiment(keyword, user_id, job.get_id())

            logging.info(f"Job ID for analysing {keyword} is {job.get_id()}")
            logging.info(f"RequestID for Job - {job.get_id()} is {request_id}")

            response["message"] = f"{keyword} was added"
            response["request_id"] = job.get_id()
            logger.info(f"Sentiment for {keyword} added successfully")
            return response, 202

        logger.info(f"User {user_id} has exhausted the quota for keywords")
        response[
            "message"
        ] = """
        Sorry!! You have exhausted the quota for keywords.
        Please remove some of the existing ones to continue.
        """
        return response, 403

    @staticmethod
    @sentiment_namespace.expect(parser, validate=True)
    @sentiment_namespace.marshal_with(sentiment_schema, as_list=True)
    def get():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            sentiment_namespace.abort(
                403, "Token required to fetch the sentiment list"
            )

        try:
            token = auth_header.split()[1]
            get_user_id_by_token(token)
            return get_all_sentiments(), 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            sentiment_namespace.abort(
                401, "Token expired. Please log in again."
            )
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            sentiment_namespace.abort(
                401, "Invalid token. Please log in again."
            )


class SentimentDetail(Resource):
    @staticmethod
    @sentiment_namespace.expect(parser, validate=True)
    # @sentiment_namespace.marshal_with(sentiment_schema)
    @sentiment_namespace.response(404, "Job <request_id> does not exist")
    def get(request_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            sentiment_namespace.abort(
                403, "Token required to fetch the sentiment"
            )

        try:
            token = auth_header.split()[1]
            get_user_id_by_token(token)

            sentiment = get_sentiment_by_id(request_id)

            if not sentiment:
                logger.info(f"Invalid request_id for token {token}")
                sentiment_namespace.abort(
                    404, f"Sentiment {request_id} does not exist"
                )

            return sentiment, 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            sentiment_namespace.abort(
                401, "Token expired. Please log in again."
            )
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            sentiment_namespace.abort(
                401, "Invalid token. Please log in again."
            )

    @staticmethod
    @sentiment_namespace.expect(parser, validate=True)
    @sentiment_namespace.response(
        404, "Sentiment <sentiment_id> does not exist"
    )
    def delete(sentiment_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            sentiment_namespace.abort(
                403, "Token required to fetch the sentiment"
            )

        try:
            token = auth_header.split()[1]
            get_user_id_by_token(token)

            sentiment = get_sentiment_by_id(sentiment_id)

            if not sentiment:
                logger.info(f"Invalid user_id for token {token}")
                sentiment_namespace.abort(
                    404, f"User {sentiment_id} does not exist"
                )

            remove_sentiment(sentiment)

            return {}, 204
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            sentiment_namespace.abort(
                401, "Token expired. Please log in again."
            )
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            sentiment_namespace.abort(
                401, "Invalid token. Please log in again."
            )

    @staticmethod
    @sentiment_namespace.expect(update_sentiment_schema, validate=True)
    # Use multiple expect blocks in swagger UI
    # @sentiment_namespace.expect(parser)
    @sentiment_namespace.marshal_with(sentiment_schema)
    @sentiment_namespace.response(
        404, "Sentiment <sentiment_id> does not exist"
    )
    def put(sentiment_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            sentiment_namespace.abort(403, "Token required to fetch the user")

        try:
            token = auth_header.split()[1]
            get_user_id_by_token(token)

            request_data = request.get_json()

            sentiment = get_sentiment_by_id(sentiment_id)

            if not sentiment:
                logger.info(f"Invalid sentiment_id for token {token}")
                sentiment_namespace.abort(
                    404, f"Sentiment {sentiment_id} does not exist"
                )

            updated_sentiment = update_sentiment(
                sentiment, request_data["keyword"]
            )

            return updated_sentiment, 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            sentiment_namespace.abort(
                401, "Token expired. Please log in again."
            )
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            sentiment_namespace.abort(
                401, "Invalid token. Please log in again."
            )


sentiment_namespace.add_resource(SentimentList, "")
sentiment_namespace.add_resource(SentimentDetail, "/<request_id>")
