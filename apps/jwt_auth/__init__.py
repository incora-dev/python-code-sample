from .shortcuts import get_user_by_token
from graphql_jwt.utils import get_authorization_header
from app.users.models import User


class JWTAuthBackend:

    def authenticate(self, request= None, **credentials):
        if request is None:
            return None

        token = get_authorization_header(request)

        if token is not None:
            return User.find_by_token(token)

        return None

    def get_user(self, user_id):
        return User.find_by_id(user_id)