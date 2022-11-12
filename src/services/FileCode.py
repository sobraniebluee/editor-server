import os.path

from src.config import Config


class FileCodeError(BaseException):
    def __init__(self, err):
        self.message = err


class FileCodeService:
    @classmethod
    def create(cls, filepath, value):
        if os.path.exists(filepath):
            raise FileCodeError("Filepath doesn't exist")
        try:
            with open(filepath, "w+") as f:
                f.write(value)
                f.close()
            return filepath
        except Exception as e:
            raise FileCodeError(e)

    @classmethod
    def update(cls, filepath, data):
        if not os.path.exists(filepath):
            raise FileCodeError("File doesn't exist")
        try:
            with open(filepath, "w+") as f:
                f.write(data)
            return True
        except Exception as e:
            raise FileCodeError(e)

    @classmethod
    def rename(cls, filepath, id_code, ext):
        if not os.path.exists(filepath):
            raise FileCodeError("File doesn't exist")
        new_filepath = f"{Config.STORAGE_PATH}/{id_code}.{ext}"
        os.rename(filepath, new_filepath)
        return new_filepath

    @classmethod
    def get_value(cls, filepath):
        if not os.path.exists(filepath):
            raise FileCodeError("File doesn't exist")
        try:
            with open(filepath, "r") as f:
                data = f.read()
            return data
        except Exception as e:
            raise FileCodeError(e)

    @classmethod
    def delete(cls, filepath):
        if not os.path.exists(filepath):
            raise FileCodeError("File doesn't exist")
        try:
            os.unlink(filepath)
        except Exception as e:
            raise FileCodeError(e)

    @classmethod
    def is_exist(cls, filepath):
        if not os.path.exists(filepath):
            return False
        else:
            return True

