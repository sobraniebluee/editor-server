import datetime


class FlaskConfig:
    SECRET = "83776601-7d7f-43f5-8ec9-bc3335fc9d2b"
    URL_PREFIX = "/api"


class Config:
    AVAILABLE_EXT = ['ts', 'js', 'txt', 'py', 'php']
    STORAGE_PATH = './storage'
    GUEST_TYPE = 'guest'
    USER_TYPE = 'user'


class OAuthGithubConfig:
    client_id = "3aafd148f366138a37e2"
    client_secret = "5a60de84c9e6480be7128bcafebb9bbc263cd1c1"
    HOST = "http://127.0.0.1:5001"
    REDIRECT_HOST = "http://127.0.0.1:3000"
    COOKIE_DEV_DOMAIN = "127.0.0.1:3000"


class TokensConfig:
    EXPIRE_FOREVER_TOKEN: datetime = datetime.timedelta(days=30)
    EXPIRE_TEMPORARY_TOKEN: datetime = datetime.timedelta(hours=24)
    # PARSE_TOKEN = 'cookies'
    PARSE_TOKEN = 'headers'


class DB:
    user = "sobranie"
    password = "root"
    database = "editor"
    host = "localhost"


class CompilerConfig:
    TIME_EXPIRE = 5
    AVAILABLE_COMPILES = ['js', 'php', 'py', 'ts']
    MAX_OUTPUT_LENGTH = 2 * 1024
