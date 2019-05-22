from flask_jwt import _jwt_required, JWTError, current_identity
from functools import wraps
from errors.article import ArticleNotFound, ArticleInvalid
from errors.error import UnauthorizedAccess

from models.article import ArticleModel


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
        # Is article_id valid
        try:
            article_id = int(kwargs['article_id'])
        except ValueError:
            return ArticleInvalid.get_response()

        article = ArticleModel.find_by_id(article_id)
        if not article:
            return ArticleNotFound.get_response()

        # Good, Are current user and article author the same
        author_id = article.author.id
        if current_identity.id != author_id:
            return UnauthorizedAccess.get_response()

        return fn(*args, **kwargs)
    return enhanced_fn
