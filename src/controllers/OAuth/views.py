from flask import Blueprint, make_response, redirect, request
from src.schemas.OAuth import OAuthParse
from src.schemas.User import UserResponse
from flask_apispec import use_kwargs, marshal_with
from src.services.OAuth import OAuthGitHub
from src.config import OAuthGithubConfig
from src.services.User import UserService
from src.middlewares.auth_required import auth_required, UserIdentify
oauth = Blueprint('oauth', __name__)


@oauth.route('/github', methods=['GET'])
@auth_required(request, optional=True)
def github_redirect(identify: UserIdentify):
    print(identify)
    if identify:
        redirect_url = f"{OAuthGithubConfig.SERVER_HOST}/api/oauth/github/authenticated?id={identify.id_user}"
        return redirect(f"https://github.com/login/oauth/authorize?client_id={OAuthGithubConfig.client_id}&redirect_uri={redirect_url}")
    else:
        return redirect(OAuthGithubConfig.HOST_CLIENT)


@oauth.route('/github/authenticated', methods=['GET'])
@use_kwargs(OAuthParse, location="query")
@marshal_with(UserResponse)
def github_authenticated(**kwargs):
    try:
        code = kwargs.get('code', None)
        id_user = kwargs.get('id', None)
        if not id_user or not code:
            return redirect(OAuthGithubConfig.HOST_CLIENT), 401

        oauth_data = OAuthGitHub.auth(code)
        user = UserService.save_forever(oauth_data=oauth_data, id_user=id_user)
        if not user:
            return "", 401
        response = make_response(redirect(OAuthGithubConfig.HOST_CLIENT))
        response.set_cookie(key='token',
                            value="Bearer " + user.tokens.access_token,
                            domain=OAuthGithubConfig.COOKIE_HOST_CLIENT,
                            # samesite='None',
                            # secure=True
                            )
        return response
    except Exception as e:
        print("Error: ", e)
        return "", 401
