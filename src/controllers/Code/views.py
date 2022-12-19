from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from src.schemas.CodeSettings import UpdateCodeSettingsRequest
from src.schemas.Code import CreateCodeRequest, UpdateCodeRequest, CodeResponse, UpdateFileRequest, LightCodeResponse
from src.services.Code import CodeService
from src.schemas.CodeSettings import CodeSettingsResponse
from src.types import SettingsT
from src.middlewares.auth_required import auth_required, UserIdentify
code = Blueprint('code', __name__)


@code.route("/list", methods=["GET"])
@auth_required(request=request)
@marshal_with(LightCodeResponse(many=True))
def all_codes(identify: UserIdentify):
    return CodeService.all_codes(id_user=identify.id_user)


@code.route("/<id_code>", methods=["GET"])
@auth_required(request=request)
@marshal_with(CodeResponse)
def get(identify: UserIdentify, id_code):
    return CodeService.get(id_user=identify.id_user, id_code=id_code)


@code.route("/create", methods=["POST"])
@auth_required(request=request)
@use_kwargs(CreateCodeRequest)
@marshal_with(CodeResponse)
def create(identify: UserIdentify, **kwargs):
    return CodeService.create(id_user=identify.id_user, **kwargs)


@code.route("/<id_code>/title", methods=["PUT"])
@auth_required(request=request)
@use_kwargs(UpdateCodeRequest)
@marshal_with(LightCodeResponse())
def set_title(identify: UserIdentify, id_code, **kwargs):
    return CodeService.set_title(id_user=identify.id_user, id_code=id_code, **kwargs)


@code.route("/<id_code>/value", methods=["PUT"])
@auth_required(request=request)
@use_kwargs(UpdateFileRequest)
@marshal_with(CodeResponse)
def set_value(identify: UserIdentify, id_code, **kwargs):
    return CodeService.set_value(id_user=identify.id_user, id_code=id_code, **kwargs)


@code.route("/<id_code>/settings", methods=["PUT"])
@auth_required(request=request)
@use_kwargs(UpdateCodeSettingsRequest)
def set_settings(identify: UserIdentify, id_code, **kwargs: SettingsT):
    return CodeService.set_settings(id_user=identify.id_user, id_code=id_code, **kwargs)


@code.route("/<id_code>", methods=["DELETE"])
@auth_required(request=request)
def delete_code(identify: UserIdentify, id_code):
    return CodeService.delete(id_user=identify.id_user, id_code=id_code)

