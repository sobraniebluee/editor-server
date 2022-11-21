from flask import Flask, jsonify
from flask_cors import CORS
from src.config import FlaskConfig, Config
from src.db import create_metadata
from src.db import session
from src.http_error import ApiBaseHttpError, NotFoundHttpError, ApiHttpError
from werkzeug.exceptions import HTTPException
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(FlaskConfig)
cors = CORS(app, resources={"*": {"origins": "*"}}, supports_credentials=True)

socketio = SocketIO(app=app,
                    async_mode="eventlet",
                    cors_allowed_origins="*",
                    cors_credentials=True,
                    path="api/socket.io")


def create_app():
    @app.errorhandler(ApiBaseHttpError)
    def api_error(error: ApiBaseHttpError):
        return error.to_dict(), error.status_code

    @app.errorhandler(HTTPException)
    def http_errors(error: HTTPException):
        error = ApiHttpError(error.description, error.code)
        return error.to_dict(), error.status_code

    @app.errorhandler(422)
    def error_422(error):
        messages = error.data.get('messages', 'Invalid request')
        if 'json' in messages:
            messages = messages['json']
        return jsonify({'message': messages}), 422

    @app.teardown_appcontext
    def end_request(*args, **kwargs):
        session.close()

    from src.controllers.Code.views import code
    from src.controllers.User.views import user
    from src.controllers.OAuth.views import oauth
    from src.controllers.Compile.views import compiles
    from src.controllers.WebSockets.views import websocket

    app.register_blueprint(code, url_prefix=f"{Config.URL_PREFIX}/code")
    app.register_blueprint(user, url_prefix=f"{Config.URL_PREFIX}/user")
    app.register_blueprint(oauth, url_prefix=f"{Config.URL_PREFIX}/oauth")
    app.register_blueprint(compiles, url_prefix=f"{Config.URL_PREFIX}/compile")
    app.register_blueprint(websocket, url_prefix=f"{Config.URL_PREFIX}/ws")

    create_metadata()

    return socketio



