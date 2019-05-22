from errors.error import Error
from status_code import Code


class CategoryError(Error):
    pass


class CategoryAlreadyExists(CategoryError):
    message = 'Category already exists'
    status_code = Code.BAD_REQUEST


class CategoryNotFound(CategoryError):
    message = 'Category not found'
    status_code = Code.NOT_FOUND
