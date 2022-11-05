from flask import Request
from src.config import FlaskConfig, TokensConfig
import jwt
import time
from src.models.User import UserTokens
from src.http_error import ApiHttpError


class UserIdentify:
    id_user: str
    type: str
    github_token: str

    def __init__(self, id_user, type, github_token=None,ext=None):
        self.id_user = id_user
        self.type = type
        self.github_token = github_token
        self._ext = ext

    def __repr__(self):
        return f"<UserIdentify type='{self.type}' id_user='{self.id_user}'/>"


class BaseErrorJWT(Exception):
    message: str

    def __init__(self):
        super().__init__(self.message)


class AbsentJWTError(BaseErrorJWT):
    message = "Please,send authorization token"


class ValueJWTError(BaseErrorJWT):
    message = "Token must start with Bearer"


class DecodeJWTError(BaseErrorJWT):
    message = "Error decode jwt"


class ExpiredJWTError(BaseErrorJWT):
    message = "Token has expired"


class BlockTokenJWTError(BaseErrorJWT):
    message = "Token has deprecated"


class CheckJWT:
    def __init__(self, request: Request, parse="cookies"):
        self.token = None
        self.identify: UserIdentify | None = None
        if parse == "cookies":
            self.jwt = request.cookies.get('token')
        if parse == "headers":
            self.jwt = request.headers.get('Authorization')
        if self.jwt:
            self.parse_jwt()
            self.decode_token()
            self.token_in_block_list()
        else:
            raise AbsentJWTError

    def parse_jwt(self):
        try:
            _, token = self.jwt.split(" ")
            self.token = token
        except ValueError as e:
            raise ValueJWTError

    def decode_token(self):
        try:
            token_decode = jwt.decode(self.token, FlaskConfig.SECRET, algorithms=["HS256"])
        except jwt.exceptions.DecodeError as e:
            raise DecodeJWTError
        if token_decode['exp'] > int(time.time() * 1000):
            raise ExpiredJWTError
        self.identify = UserIdentify(token_decode['id'], token_decode['type'], token_decode.get('github_token', None))

    def token_in_block_list(self):
        token = UserTokens.query.filter(UserTokens.id_user == self.identify.id_user, UserTokens.access_token == self.token).first()
        if not token:
            raise BlockTokenJWTError


def auth_required(request: Request, optional=False):
    def decorate_function(func):
        def decorate_params(*args, **kwargs):
            try:
                result = CheckJWT(request, parse=TokensConfig.PARSE_TOKEN)
                identify = result.identify
            except Exception as e:
                if not optional:
                    raise ApiHttpError(message=str(e), status_code=401)
                else:
                    identify = None

            return func(identify=identify, *args, **kwargs)
        decorate_params.__name__ = func.__name__
        return decorate_params
    return decorate_function
