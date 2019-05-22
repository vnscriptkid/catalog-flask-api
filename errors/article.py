from errors.error import Error
from status_code import Code


class ArticleError(Error):
    pass


class ArticleAlreadyExists(ArticleError):
    message = 'Article already exists'
    status_code = Code.BAD_REQUEST


class ArticleNotFound(ArticleError):
    message = 'Article not found'
    status_code = Code.NOT_FOUND


class ArticleInvalid(ArticleError):
    message = 'Article invalid'
    status_code = Code.BAD_REQUEST
