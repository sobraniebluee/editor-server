import datetime

import jwt
from sqlalchemy.orm import relationship

from src.config import TokensConfig, Config
from src.db import db, Base, session
from src.models.mixins import Timestamp
from src.utils import get_random_char_id


class UserTokens(Base):
    __tablename__ = 'user_tokens'

    id_user = db.Column(db.VARCHAR(18), db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    access_token = db.Column(db.VARCHAR(256), nullable=True)

    def __init__(self, id_user):
        self.id_user = id_user

    def create_access_token(self, payload, exp):
        payload["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + exp
        self.access_token = jwt.encode(payload=payload, key=TokensConfig.SECRET_JWT, algorithm="HS256")
        self.commit()

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise


class UserModel(Base, Timestamp):
    __tablename__ = 'users'

    id = db.Column(db.VARCHAR(18), primary_key=True)
    oauth_id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.VARCHAR(128), nullable=True)
    user_type = db.Column(db.CHAR(10), nullable=False)
    avatar_url = db.Column(db.VARCHAR(256), nullable=True)
    ip = db.Column(db.VARCHAR(14), nullable=True)
    tokens = relationship("UserTokens",  backref="users", uselist=False, passive_deletes=True)

    def __init__(self):
        self.id = get_random_char_id()
        self.user_type = Config.GUEST_TYPE
        self.ip = None
        self.username = None
        self.oauth_id = None
        self.avatar = None

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    def update(self, username, oauth_id, avatar):
        try:
            self.oauth_id = oauth_id
            self.avatar_url = avatar
            self.username = username
            self.user_type = Config.USER_TYPE
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
        except Exception as e:
            session.rollback()
            raise

    def __repr__(self):
        return f"<User id='{self.id}' oauth_id='{self.oauth_id}' user_type='{self.user_type}' >"