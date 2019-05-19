class UserException(BaseException):
    pass


class UserNotFound(UserException):
    msg = "User Not Found"


class UserAlreadyExists(UserException):
    msg = "User already exists"


