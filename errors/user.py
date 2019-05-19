class UserException(BaseException):
    pass


class UserNotFound(UserException):
    pass


class UserAlreadyExists(UserException):
    pass


