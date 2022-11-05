from src.http_error import ApiHttpError


class Error:
    @classmethod
    def server_error(cls, msg="Server error"):
        raise ApiHttpError(message=msg, status_code=500)

    @classmethod
    def error_not_found(cls, msg='Not found', status_code=404):
        raise ApiHttpError(message=msg, status_code=status_code)

    @classmethod
    def error_default(cls, msg, status_code):
        raise ApiHttpError(message=msg, status_code=status_code)
