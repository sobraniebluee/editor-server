import datetime
from os import environ, path
from dotenv import load_dotenv


if not load_dotenv(path.join(path.abspath(path.curdir), '.env')):
    exit("Error load environ!")


class FlaskConfig:
    SECRET = "83776601-7d7f-43f5-8ec9-bc3335fc9d2b"
    SERVER_NAME = '127.0.0.1:5001'
    PREFERRED_URL_SCHEME = 'http'


class DevFlaskConfig(FlaskConfig):
    DEBUG = True
    ENV = 'development'
    TESTING = True


class ProdFlaskConfig(FlaskConfig):
    DEBUG = False
    ENV = 'production'
    TESTING = True


class Config:
    AVAILABLE_EXT = ['ts', 'js', 'txt', 'py', 'php']
    STORAGE_PATH = './storage'
    GUEST_TYPE = 'guest'
    USER_TYPE = 'user'
    URL_PREFIX = '/api'


class OAuthGithubConfig:
    client_id = "3aafd148f366138a37e2"
    client_secret = "5a60de84c9e6480be7128bcafebb9bbc263cd1c1"
    SERVER_HOST = f"{FlaskConfig.PREFERRED_URL_SCHEME}://{FlaskConfig.SERVER_NAME}"
    REDIRECT_HOST_CLIENT = "http://127.0.0.1:3000"
    # change for real domain
    COOKIE_DOMAIN = environ.get('COOKIE_DEV_DOMAIN')


class TokensConfig:
    EXPIRE_FOREVER_TOKEN: datetime = datetime.timedelta(days=30)
    EXPIRE_TEMPORARY_TOKEN: datetime = datetime.timedelta(hours=24)
    SECRET_JWT = "83776601-7d7f-43f5-8ec9-bc3335fc9d2b"
    PARSE_TOKEN = "cookies"


class DBConfig:
    DB_USER = environ.get('DB_USER')
    DB_PASSWD = environ.get('DB_PASSWD')
    DB_NAME = environ.get('DB_NAME')
    DB_HOST = environ.get('DB_HOST')
    DB_URL_CONNECT = f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_NAME}?charset=utf8"


class CompilerConfig:
    TIME_EXPIRE = 5
    AVAILABLE_COMPILES = ['js', 'php', 'py', 'ts']
    MAX_OUTPUT_LENGTH = 2 * 1024
