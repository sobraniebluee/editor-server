from flask import Blueprint, request
from src.middlewares.auth_required import auth_required, UserIdentify
from flask_apispec import marshal_with, use_kwargs
from src.services.Compile import CompileService
from src.schemas.Compile import OutputCompileResponse
compiles = Blueprint('compile', __name__)


@compiles.route('/<id_file>', methods=['POST'])
@auth_required(request=request)
@marshal_with(OutputCompileResponse)
def compile_file(identify: UserIdentify, id_file):
    return CompileService.compile(id_user=identify.id_user, id_file=id_file)



