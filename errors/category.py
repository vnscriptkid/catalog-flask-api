class CategoryError(BaseException):
    pass


class CategoryAlreadyExists(CategoryError):
    msg = 'Category already exists'


class CategoryNotFound(CategoryError):
    msg = 'Category not found'
