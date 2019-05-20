from flask_restplus import Namespace, Resource
from marshmallow import ValidationError
from flask_jwt import current_identity

from schemas.article import article_schema, articles_schema
from models.article import ArticleModel
from decorators.authorization import jwt_needed, must_be_author
from errors.category import CategoryNotFound

api = Namespace('articles', description="Article operations")


@api.route('/')
class ArticleList(Resource):
    @staticmethod
    def get():
        print('current user: ', current_identity)
        arts = ArticleModel.get_all()
        try:
            output = articles_schema.dump(arts)
        except ValidationError as err:
            return err.messages, 422
        return output.data, 200

    @jwt_needed
    def post(self):
        # Get json data, attach author id
        try:
            data = api.payload
            data['author_id'] = current_identity.id
        except:
            return {'msg': 'Bad Request'}, 400

        # Is data coming in valid
        try:
            result = article_schema.load(data)
        except ValidationError as err:
            return err.messages, 422

        # Good, save to db
        try:
            art = ArticleModel(**result.data)
            art.save()
        except CategoryNotFound as err:
            return {'msg': err.msg}, 404
        except:
            return {'msg': 'Can not save the article to db'}, 500

        # Is data coming out valid
        try:
            output = article_schema.dump(art)
        except ValidationError as err:
            return err.messages, 422

        # Good, successful
        return output.data, 201


@api.route('/<author_id>')
class Article(Resource):
    @jwt_needed
    @must_be_author
    def get(self, author_id):
        art = ArticleModel.find_by_id(author_id)
        if art is None:
            return {'msg': 'Article not found'}, 404
        try:
            output = article_schema.dump(art)
        except ValidationError as err:
            return err.messages, 422

        return output.data, 200

    @jwt_needed
    @must_be_author
    def delete(self, author_id):
        art = ArticleModel.find_by_id(author_id)
        if art is None:
            return {'msg': 'Article not found'}, 404
        try:
            art.delete()
        except:
            return {'msg': 'Can not delete the article'}, 500
        return {'success': True, 'author_id': 'The article has been deleted'}, 204

    @jwt_needed
    @must_be_author
    def update(self, author_id):
        art = ArticleModel.find_by_id(author_id)
        if art is None:
            return {'msg': 'Article not found'}, 404
        try:
            data = api.payload
        except:
            return {'msg': 'Bad requests'}, 400
        try:
            result = article_schema.load(data)
        except ValidationError as err:
            return err.messages, 422

        try:
            art.updateProps(**result.data)
            art.save()
        except ReferenceError as refError:
            return {'msg': refError.args}, 404
        except:
            return {'msg': 'Can not save the article to db'}, 500

        try:
            output = article_schema.dump(art)
        except ValidationError as err:
            return err.messages, 422

        return output.data, 200






