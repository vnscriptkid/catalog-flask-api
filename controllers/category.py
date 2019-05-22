from flask_restplus import Namespace, Resource
from marshmallow import ValidationError

from models.category import CategoryModel
from models.article import ArticleModel
from schemas.category import categories_schema, category_schema
from schemas.article import articles_schema
from errors.category import CategoryNotFound
from errors.error import ServerError

api = Namespace('categories', description="Category operations")


@api.route('/')
class CategoryList(Resource):
    @staticmethod
    def get():
        categories = CategoryModel.get_all()

        # Make sure to show only what should be
        output = categories_schema.dump(categories)

        return output.data


@api.route('/<_id>/articles')
class ArticlesInCategory(Resource):
    @staticmethod
    def get(_id):
        # Does category_id exist
        category = CategoryModel.find_by_id(_id)
        if not category:
            return CategoryNotFound.get_response()

        # Good, pull all articles with that category
        try:
            articles = ArticleModel.find_by_cat(category)
        except:
            return ServerError.get_response()

        # Show only what should be showed
        output = articles_schema.dump(articles)

        # Good, send back
        return output.data

