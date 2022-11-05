from flask import Flask, jsonify
from flask_cors import CORS
from src.config import FlaskConfig
from src.db import create_metadata
from src.db import session
from src.http_error import BaseHttpError, NotFoundHttpError


def create_app():
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)
    cors = CORS(app, resources={"*": {"origins": "*"}}, supports_credentials=True)

    @app.errorhandler(BaseHttpError)
    def api_error(error: BaseHttpError):
        return error.to_dict(), error.status_code

    @app.errorhandler(422)
    def error_422(error):
        messages = error.data.get('messages', 'Invalid request')
        print(error.data)
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

    app.register_blueprint(code, url_prefix=f"{FlaskConfig.URL_PREFIX}/code")
    app.register_blueprint(user, url_prefix=f"{FlaskConfig.URL_PREFIX}/user")
    app.register_blueprint(oauth, url_prefix=f"{FlaskConfig.URL_PREFIX}/oauth")
    app.register_blueprint(compiles, url_prefix=f"{FlaskConfig.URL_PREFIX}/compile")

    create_metadata()

    return app



