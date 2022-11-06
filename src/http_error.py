class ApiBaseHttpError(Exception):
    status_code: int
    message: str

    def __init__(self):
        super(ApiBaseHttpError, self).__init__(self.message, self.status_code)

    def to_dict(self):
        response = dict()
        response['message'] = self.message
        return response


class ApiHttpError(ApiBaseHttpError):
    status_code: int
    message: str

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class NotFoundHttpError(ApiBaseHttpError):
    status_code = 404
    message = "Not found"


class ServerHttpError(ApiBaseHttpError):
    status_code = 500
    message = "Server error"

