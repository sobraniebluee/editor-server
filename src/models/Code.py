from src.models.mixins import Timestamp
from src.utils import get_random_char_id
from src.services.files.FileCode import FileCodeService, FileCodeError
from sqlalchemy.orm import relationship
from src.http_error import NotFoundHttpError, ServerHttpError

from src.db import Base, db, session
from src.config import Config, CompilerConfig


class CodeSettingsModel(Base):
    __tablename__ = "settings"

    id_code = db.Column(db.VARCHAR(32), db.ForeignKey('codes.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    live_mode = db.Column(db.Boolean(), nullable=False, default=False)
    password = db.Column(db.VARCHAR(64), nullable=True, default=None)
    read_only = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, id_code):
        self.id_code = id_code

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def __repr__(self):
        return f"<CodeSettings id_code='self.id_code' live_mode={self.live_mode} read_only={self.read_only}>"


class CodeModel(Base, Timestamp):
    __tablename__ = 'codes'

    id = db.Column(db.VARCHAR(20), primary_key=True, nullable=False)
    id_user = db.Column(db.VARCHAR(18), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    filepath = db.Column(db.VARCHAR(256), nullable=False)
    title = db.Column(db.VARCHAR(32), nullable=False)
    ext = db.Column(db.CHAR(6), nullable=False)
    settings = relationship('CodeSettingsModel', backref='codes', uselist=False, passive_deletes=True)

    def __init__(self, id_user, title, ext):
        id_code = get_random_char_id()
        self.id = id_code
        self.title = title
        self.ext = ext
        self.id_user = id_user
        self.filepath = f"{Config.STORAGE_PATH}/{id_code}.{ext}"

    @property
    def is_executable(self):
        return self.ext in CompilerConfig.AVAILABLE_COMPILES

    @property
    def value(self):
        try:
            return FileCodeService.get_value(self.filepath)
        except FileCodeError:
            raise NotFoundHttpError

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise ServerHttpError

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise ServerHttpError

    def __repr__(self):
        return f"<Code id='{self.id}' title='{self.title}' ext='{self.ext}'>"
