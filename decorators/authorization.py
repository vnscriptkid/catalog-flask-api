from flask_jwt import _jwt_required, JWTError
from functools import wraps


def jwt_needed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            _jwt_required(None)
        except JWTError as err:
            return {err.error: err.description}, 499
        return fn(*args, **kwargs)

    return wrapper
