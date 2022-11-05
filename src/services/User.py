from src.config import Config, TokensConfig
from src.middlewares.error import Error
from src.models.User import UserModel, UserTokens
from src.services.OAuth import OAuthResponse
from src.http_error import NotFoundHttpError, ServerHttpError


class UserService:
    @classmethod
    def save_temporary(cls):
        temp_user = UserModel(user_type=Config.GUEST_TYPE)
        temp_token = UserTokens(temp_user.id)
        token_payload = {
            'type': 'guest',
            'id': temp_user.id,
        }
        temp_token.create_access_token(payload=token_payload, exp=TokensConfig.EXPIRE_TEMPORARY_TOKEN)
        temp_user.save()
        temp_token.save()
        return temp_user, 200

    @classmethod
    def save_forever(cls, oauth_data: OAuthResponse, id_user: str):
        user = UserModel.query.filter(UserModel.oauth_id == oauth_data.id).first()

        if not user:
            user = UserModel.query.filter(UserModel.id == id_user).first()
        else:
            temp_user = UserModel.query.filter(UserModel.id == id_user).first()
            temp_user.delete()

        user.update(username=oauth_data.login,
                    oauth_id=oauth_data.id,
                    avatar=oauth_data.avatar)
        token = UserTokens.query.filter(UserTokens.id_user == user.id).first()
        token.create_access_token(payload={
            'github_token': oauth_data.access_token,
            'type': Config.USER_TYPE,
            'id': user.id
        }, exp=TokensConfig.EXPIRE_FOREVER_TOKEN)
        token.commit()
        return user

    @classmethod
    def get_one(cls, id_user):
        user = UserModel.query.filter(UserModel.id == id_user).first()
        if not user:
            return Error.error_not_found()
        return user, 200

    @classmethod
    def logout(cls, id_user):
        user = UserModel.query.filter(UserModel.id == id_user).first()
        if not user:
            return Error.error_not_found()
        tokens = UserTokens.query.filter(UserTokens.id_user == id_user).first()
        setattr(tokens, 'access_token', None)
        tokens.commit()
        return "", 204
