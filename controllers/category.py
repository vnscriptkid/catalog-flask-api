from flask_restplus import Namespace, Resource
from marshmallow import ValidationError

from models.category import CategoryModel
from models.article import ArticleModel
from schemas.category import category_schema, categories_schema
from schemas.article import articles_schema
from errors.category import CategoryAlreadyExists

api = Namespace('categories', description="Article operations")


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

    @staticmethod
    def post():
        try:
            data = api.payload  # dict type
        # TODO: more specific error
        except:
            return {'msg': 'Bad Request'}, 400
        try:
            result = category_schema.load(data)
        except ValidationError as err:
            return err.messages, 422

        # name = result.data['name']

        try:
            cat = CategoryModel(**result.data)
            cat.save()
        except CategoryAlreadyExists as err:
            return {'msg': err.msg}, 409
        except:
            return {'msg': 'Can not save the Category'}, 500

        try:
            output = category_schema.dump(cat)
        except ValidationError as err:
            return err.messages, 422

        return output.data, 201


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


@api.route('/<_id>/articles')
class ArticlesInCategory(Resource):
    @staticmethod
    def get(_id):
        cat = CategoryModel.find_by_id(_id)
        if not cat:
            return {'msg': 'Category not found'}, 404
        try:
            arts = ArticleModel.find_by_cat(cat)
        except:
            return {'msg': 'Can not find articles'}, 500
        try:
            output = articles_schema.dump(arts)
        except ValidationError as err:
            return err.messages, 422
        return output.data, 200



