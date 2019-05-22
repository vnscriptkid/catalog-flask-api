class ArticleError(BaseException):
    pass


class ArticleAlreadyExists(ArticleError):
    msg = 'Article already exists'


class ArticleNotFound(ArticleError):
    msg = 'Article not found'
