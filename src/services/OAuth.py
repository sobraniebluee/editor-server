from typing import Dict, Any

import requests
from src.config import OAuthGithubConfig


class OAuthError(BaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class OAuthResponse:
    def __init__(self, login, avatar, id, access_token):
        self.login = login
        self.avatar = avatar
        self.id = id
        self.access_token = access_token


class OAuthGitHub:
    @classmethod
    def auth(cls, code) -> OAuthResponse:
        try:
            access_token = cls.get_access_token(code)
            user_data = cls.get_user_data(access_token)
            if user_data:
                return OAuthResponse(**user_data)
        except OAuthError as e:
            raise e

    @classmethod
    def get_access_token(cls, code):
        response_access_token = requests.post(
            f"https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": OAuthGithubConfig.client_id,
                "client_secret": OAuthGithubConfig.client_secret,
                "code": code,
            })
        if response_access_token.status_code == 200:
            return response_access_token.json()['access_token']
        else:
            raise OAuthError(message=response_access_token.text)

    @classmethod
    def get_user_data(cls, access_token) -> dict[str, Any]:
        response_user_data = requests.get(
            'https://api.github.com/user',
            headers={
                "Authorization": "Bearer " + access_token
            })
        if response_user_data.status_code == 200:
            user_data = response_user_data.json()
            return {
                'avatar': user_data['avatar_url'],
                'login': user_data['login'],
                'access_token': access_token,
                'id': user_data['id']
            }
        else:
            raise OAuthError(message=response_user_data.text)
