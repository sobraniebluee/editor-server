from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from src.config import FlaskConfig, Config
from src.db import create_metadata
from src.db import session
from src.http_error import ApiBaseHttpError, ApiHttpError
from src.logger import Logger
from src.middlewares.auth_required import auth_required, UserIdentify


logger = Logger(__name__)
app = Flask(__name__)
app.config.from_object(FlaskConfig)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

socketio = SocketIO(app=app,
                    async_mode="eventlet",
                    cors_allowed_origins="*",
                    cors_credentials=True,
                    path="api/socket.io")


def create_app():
    @app.errorhandler(SQLAlchemyError)
    def database_error(error: SQLAlchemyError):
        logger.db_error.critical(f"DATABASE ERROR: {error}")
        return jsonify({"message": "Server error db!"}), 500

    @app.errorhandler(ApiBaseHttpError)
    @auth_required(request=request, optional=True)
    def api_errors(error: ApiBaseHttpError, identify: UserIdentify):
        logger.api_error.warning(
            f"in '{request.method} {request.path}' RES: {error.message} {error.status_code} IP [{request.host}] USER: {identify}")
        return error.to_dict(), error.status_code

    @app.errorhandler(HTTPException)
    @auth_required(request=request, optional=True)
    def http_errors(error: HTTPException, identify: UserIdentify):
        response_error = ApiHttpError(error.description, error.code)
        logger.api_error.error(
            f"in '{request.method} {request.path}' RES: {error.description} {error.code} IP [{request.host}] USER: {identify}")
        return response_error.to_dict(), response_error.status_code

    @app.errorhandler(422)
    def error_422(error):
        messages = error.data.get('messages', 'Invalid request')
        if 'json' in messages:
            messages = messages['json']
        return jsonify({'message': messages}), 422

    @app.teardown_appcontext
    def end_request(*args, **kwargs):
        session.close()

    @app.after_request
    @auth_required(request=request, optional=True)
    def after_req(response: Response, identify: UserIdentify):
        print('info')
        logger.api_info.info(
            f"in '{request.method} {request.path}' CODE: {response.status_code} IP [{request.host}] USER: {identify}")

        return response

    from src.controllers.Code.views import code
    from src.controllers.User.views import user
    from src.controllers.OAuth.views import oauth
    from src.controllers.Compile.views import compiles
    from src.controllers.WebSocket.views import websocket

    app.register_blueprint(code, url_prefix=f"{Config.URL_PREFIX}/code")
    app.register_blueprint(user, url_prefix=f"{Config.URL_PREFIX}/user")
    app.register_blueprint(oauth, url_prefix=f"{Config.URL_PREFIX}/oauth")
    app.register_blueprint(compiles, url_prefix=f"{Config.URL_PREFIX}/compile")
    app.register_blueprint(websocket, url_prefix=f"{Config.URL_PREFIX}/ws")

    create_metadata()

    return socketio



