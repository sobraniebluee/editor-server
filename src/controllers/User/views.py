from flask import Blueprint, request, make_response, jsonify

from src.middlewares.auth_required import auth_required
from src.schemas.User import UserResponse
from src.services.User import UserService
from src.middlewares.auth_required import UserIdentify

user = Blueprint('user', __name__)


@user.route("/auth", methods=["GET"])
@auth_required(request=request, optional=True)
def auth(identify: UserIdentify):
    schema = UserResponse()
    if not identify:
        data, status_code = UserService.save_temporary()
        if status_code != 200:
            return jsonify(data), status_code
        response = make_response(schema.dump(data), status_code)
        response.set_cookie('token', 'Bearer ' + data.tokens.access_token)
        return response
    else:
        data, status_code = UserService.get_one(identify.id_user)
        if status_code != 200:
            return jsonify(data), status_code
        return make_response(schema.dump(data), status_code)


@user.route("/logout", methods=['DELETE'])
@auth_required(request=request)
def logout(identify: UserIdentify):
    return UserService.logout(id_user=identify.id_user)
