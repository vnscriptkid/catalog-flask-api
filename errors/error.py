from status_code import Code


class Error(BaseException):
    @classmethod
    def get_response(cls, error=None):
        if cls.message:
            json_response = {'message': cls.message}
        if error:
            json_response['error'] = error
        return json_response, cls.status_code


class ServerError(Error):
    status_code = Code.SERVER_ERROR
    message = "Server error"


class UnauthorizedAccess(Error):
    status_code = Code.UNAUTHORIZED
    message = "Unauthorized access"
