import logging

from flask import current_app
from flask import request
from flask_restx import Resource
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError

from app.api.auth.crud import get_user_id_by_token
from app.api.auth.serializers import parser
from app.api.users.crud import get_all_users
from app.api.users.crud import get_user_by_id
from app.api.users.crud import remove_user
from app.api.users.crud import update_user
from app.api.users.serializers import parser as user_parser
from app.api.users.serializers import user_readable
from app.api.users.serializers import users_namespace


logger = logging.getLogger(__name__)


class UsersList(Resource):
    @staticmethod
    @users_namespace.expect(user_parser, validate=True)
    @users_namespace.marshal_with(user_readable, as_list=True)
    def get():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user list")

        try:
            token = auth_header.split()[1]

            get_user_id_by_token(token)

            args = user_parser.parse_args()
            page = int(args.get("page", 1))
            per_page = current_app.config.get("POSTS_PER_PAGE")

            users = get_all_users(page, per_page)
            return users.items, 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")


class UsersDetail(Resource):
    @staticmethod
    @users_namespace.expect(parser, validate=True)
    @users_namespace.marshal_with(user_readable)
    @users_namespace.response(404, "User <user_id> does not exist")
    def get(user_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user")

        try:
            token = auth_header.split()[1]

            get_user_id_by_token(token)

            user = get_user_by_id(user_id)

            if not user:
                logger.info(f"Invalid user_id for token {token}")
                users_namespace.abort(404, f"User {user_id} does not exist")

            return user, 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")

    @staticmethod
    @users_namespace.expect(parser, validate=True)
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(user_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user")

        try:
            token = auth_header.split()[1]

            get_user_id_by_token(token)

            user = get_user_by_id(user_id)

            if not user:
                logger.info(f"Invalid user_id for token {token}")
                users_namespace.abort(404, f"User {user_id} does not exist")

            remove_user(user)

            return {}, 204
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")

    @staticmethod
    @users_namespace.expect(user_readable, validate=True)
    # Use multiple expect blocks in swagger UI
    # @users_namespace.expect(parser)
    @users_namespace.marshal_with(user_readable)
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(user_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.info(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user")

        try:
            token = auth_header.split()[1]

            get_user_id_by_token(token)

            request_data = request.get_json()

            user = get_user_by_id(user_id)

            if not user:
                logger.info(f"Invalid user_id for token {token}")
                users_namespace.abort(404, f"User {user_id} does not exist")

            updated_user = update_user(
                user, request_data["username"], request_data["email"]
            )

            return updated_user, 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {token} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except InvalidTokenError:
            logger.error(f"Auth-token {token} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(UsersDetail, "/<int:user_id>")
