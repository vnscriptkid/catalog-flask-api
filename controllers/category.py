from flask_restplus import Namespace, Resource
from marshmallow import ValidationError

from models.category import CategoryModel
from models.article import ArticleModel
from schemas.category import categories_schema, category_schema
from schemas.article import articles_schema

api = Namespace('categories', description="Category operations")


@api.route('/')
class CategoryList(Resource):
    @staticmethod
    def get():
        cats = CategoryModel.get_all()
        try:
            output = categories_schema.dump(cats)
        except ValidationError as err:
            return err.messages, 422
        return output.data, 200


@api.route('/<_id>/articles')
class ArticlesInCategory(Resource):
    @staticmethod
    def get(_id):
        # Does category_id exist
        cat = CategoryModel.find_by_id(_id)
        if not cat:
            return {'msg': 'Category not found'}, 404

        # Good, pull all articles with that category
        try:
            arts = ArticleModel.find_by_cat(cat)
        except:
            return {'msg': 'Can not find articles'}, 500

        # Is data coming out good?
        try:
            output = articles_schema.dump(arts)
        except ValidationError as err:
            return err.messages, 422

        # Good, successful
        return output.data, 200


@api.route('/<_id>')
class Category(Resource):
    @staticmethod
    def get(_id):
        cat = CategoryModel.find_by_id(_id)
        if not cat:
            return {'msg': 'Category not found'}, 404
        try:
            output = category_schema.dump(cat)
        except ValidationError as err:
            return err.messages, 422
        return output.data, 200
