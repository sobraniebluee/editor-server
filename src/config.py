import datetime
from os import environ, path
from dotenv import load_dotenv

if not load_dotenv(path.join(path.abspath(path.curdir), '.env')):
    exit("Error load environ!")


class FlaskConfig:
    TESTING = True
    SECRET_KEY = "aecdc6b4-848a-4d79-89c4-e7eabd5ed62a"
    SERVER_NAME = environ.get("SERVER_NAME")
    PREFERRED_URL_SCHEME = "http"
    ENV = environ.get("ENV")


class Config:
    AVAILABLE_EXT = ["ts", "js", "txt", "py", "php"]
    STORAGE_PATH = environ.get('STORAGE_PATH')
    GUEST_TYPE = "guest"
    USER_TYPE = "user"
    URL_PREFIX = "/api"


class OAuthGithubConfig:
    client_id = "3aafd148f366138a37e2"
    client_secret = "5a60de84c9e6480be7128bcafebb9bbc263cd1c1"
    SERVER_HOST = f"{FlaskConfig.PREFERRED_URL_SCHEME}://{FlaskConfig.SERVER_NAME}"
    HOST_CLIENT = environ.get("HOST_CLIENT")
    COOKIE_HOST_CLIENT = environ.get("COOKIE_HOST_CLIENT")


class TokensConfig:
    EXPIRE_FOREVER_TOKEN: datetime = datetime.timedelta(days=30)
    EXPIRE_TEMPORARY_TOKEN: datetime = datetime.timedelta(hours=24)
    SECRET_JWT = "b4a5d3e7-c794-439f-ac83-5e1c55b0be4b"
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
    MAX_OUTPUT_LENGTH = 5 * 1024
    TYPESCRIPT_CMD = 'tsc'
    TYPESCRIPT_VERSION = 'typescript@4.5.4'
    NODE_CMD = 'node'
    NODE_VERSION = 'node@v18.12.1'
    PYTHON_CMD = 'python3'
    PYTHON_VERSION = 'python@3.10.2'
    PHP_CMD = 'php'
    PHP_VERSION = 'php@8.1.10'
