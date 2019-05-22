from errors.error import Error
from status_code import Code


class UserException(Error):
    pass


class UserNotFound(UserException):
    message = "User Not Found"
    status_code = Code.NOT_FOUND


class UserAlreadyExists(UserException):
    message = "User already exists"
    status_code = Code.BAD_REQUEST
