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
            article = ArticleModel(**result.data)
            article.save()
        except CategoryNotFound as err:
            return {'msg': err.msg}, 404
        except:
            return {'msg': 'Can not save the article to db'}, 500

        # Is data coming out valid
        try:
            output = article_schema.dump(article)
        except ValidationError as err:
            return err.messages, 422

        # Good, successful
        return output.data, 201


@api.route('/<article_id>')
class Article(Resource):
    @staticmethod
    def get(article_id):
        article = ArticleModel.find_by_id(article_id)
        if article is None:
            return {'msg': 'Article not found'}, 404
        try:
            output = article_schema.dump(article)
        except ValidationError as err:
            return err.messages, 422

        return output.data, 200

    @jwt_needed
    @must_be_author
    def delete(self, article_id):
        # Does article_id exi
        article = ArticleModel.find_by_id(article_id)
        if article is None:
            return {'msg': 'Article not found'}, 404
        try:
            article.delete()
        except:
            return {'msg': 'Can not delete the article'}, 500

        return {'success': True}, 204

    @jwt_needed
    @must_be_author
    def put(self, article_id):
        # Does article_id exist?
        article = ArticleModel.find_by_id(article_id)
        if article is None:
            return {'msg': 'Article not found'}, 404

        # Is data coming in good?
        try:
            data = api.payload
            data['author_id'] = current_identity.id
        except:
            return {'msg': 'Bad requests'}, 400
        try:
            result = article_schema.load(data)
        except ValidationError as err:
            return err.messages, 422

        # update to db
        try:
            article.update_props(**result.data)
            article.save()
        except CategoryNotFound as err:
            return {'msg': err.msg}, 404
        except:
            return {'msg': 'Can not save the article to db'}, 500

        # is data coming out good?
        try:
            output = article_schema.dump(article)
        except ValidationError as err:
            return err.messages, 422

        # Good, successful
        return output.data, 200
