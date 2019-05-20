from flask_jwt import _jwt_required, JWTError, current_identity
from functools import wraps
from flask import request


def jwt_needed(fn):
    @wraps(fn)
    def enhanced_fn(*args, **kwargs):
        try:
            _jwt_required(None)
        except JWTError as err:
            return {err.error: err.description}, 499
        return fn(*args, **kwargs)

    return enhanced_fn


# This decorator must come after jwt_needed
def must_be_author(fn):
    @wraps(fn)
    def enhanced_fn(*args, **kwargs):
        author_id = int(kwargs['author_id'])
        if current_identity.id != author_id:
            return {'msg': 'Unauthorized access'}, 401
        return fn(*args, **kwargs)
    return enhanced_fn


# For reference
def require_jwt(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'msg': 'Token is needed'}, 499

        if token != 'abc':
            return {'msg': 'Token is invalid'}, 498

        return fn(*args, **kwargs)

    return decorated

