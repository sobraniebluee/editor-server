from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from src.http_error import NotFoundHttpError, ServerHttpError, PermissionDenied
from src.models.Code import CodeModel, CodeSettingsModel
from src.services.files.FileCode import FileCodeService, FileCodeError
from src.types import SettingsT


class CodeService:
    @classmethod
    def all_codes(cls, id_user):
        return CodeModel.query.filter(CodeModel.id_user == id_user).order_by(desc(CodeModel.updated_at), desc(CodeModel.created_at)).all()

    @classmethod
    def create(cls, id_user, title, ext, value):
        new_code = CodeModel(title=title, ext=ext, id_user=id_user)
        new_code_settings = CodeSettingsModel(new_code.id)
        try:
            FileCodeService.create(new_code.filepath, value=value)
            new_code.save()
            new_code_settings.save()
            return new_code, 200
        except SQLAlchemyError as e:
            if new_code.filepath:
                FileCodeService.delete(new_code.filepath)
            raise SQLAlchemyError(e)
        except FileCodeError as e:
            raise ServerHttpError

    @classmethod
    def get(cls, id_user, id_code):
        record = CodeModel.get(id_code=id_code, id_user=id_user)
        return record, 200

    @classmethod
    def delete(cls, id_user, id_code):
        record: CodeModel = CodeModel.get(id_code=id_code, id_user=id_user)
        if not record.is_owner:
            raise PermissionDenied
        try:
            FileCodeService.delete(record.filepath)
            record.delete()
        except SQLAlchemyError as e:
            FileCodeService.delete(record.filepath)
            print("Error delete code", e)
            raise NotFoundHttpError
        except FileCodeError as e:
            record.delete()
            raise NotFoundHttpError
        return "", 204

    @classmethod
    def set_value(cls, id_user, id_code, value):
        record: CodeModel = CodeModel.get(id_code=id_code, id_user=id_user)
        if record.settings.read_only and not record.is_owner:
            raise PermissionDenied
        if not record:
            raise NotFoundHttpError
        try:
            FileCodeService.update(filepath=record.filepath, data=value)
            return "", 204
        except FileCodeError:
            print("Error update code")
            raise ServerHttpError

    @classmethod
    def set_title(cls, id_user, id_code, title, ext):
        record: CodeModel = CodeModel.get(id_code=id_code, id_user=id_user)
        if record.settings.read_only and not record.is_owner:
            raise PermissionDenied
        try:
            new_filepath = FileCodeService.rename(record.filepath, id_code, ext)
        except FileCodeError:
            # print("Error rename")
            raise ServerHttpError
        if new_filepath != record.filepath:
            setattr(record, "ext", ext)
            setattr(record, "filepath", new_filepath)
        setattr(record, "title", title)
        record.commit()
        return record, 200

    @classmethod
    def set_settings(cls, id_user, id_code, **kwargs: SettingsT):
        record: CodeModel = CodeModel.get(id_code=id_code, id_user=id_user)
        if not record.is_owner:
            raise PermissionDenied
        settings = CodeSettingsModel.query.filter(CodeSettingsModel.id_code == id_code).first()
        if not settings:
            raise NotFoundHttpError
        for key in kwargs:
            if key != "password":
                setattr(settings, key, kwargs[key])

        password = kwargs.get("password", None)
        setattr(settings, "password", password)

        try:
            settings.commit()
            return "", 204
        except Exception as e:
            print("Error update settings")
            raise ServerHttpError




