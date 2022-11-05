class BaseHttpError(Exception):
    status_code: int
    message: str

    def __init__(self):
        super(BaseHttpError, self).__init__(self.message, self.status_code)

    def to_dict(self):
        response = dict()
        response['message'] = self.message
        return response


class ApiHttpError(BaseHttpError):
    status_code: int
    message: str

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class NotFoundHttpError(BaseHttpError):
    status_code = 404
    message = "Not found"


class ServerHttpError(BaseHttpError):
    status_code = 500
    message = "Server error"

