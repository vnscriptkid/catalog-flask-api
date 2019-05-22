from flask_restplus import Namespace, Resource
from marshmallow import ValidationError
from flask_jwt import current_identity

from schemas.article import article_schema, articles_schema
from models.article import ArticleModel
from decorators.authorization import jwt_needed, must_be_author
from errors.category import CategoryNotFound
from errors.article import ArticleNotFound, ArticleInvalid
from errors.error import ServerError

api = Namespace('articles', description="Article operations")


@api.route('/')
class ArticleList(Resource):
    @staticmethod
    def get():
        articles = ArticleModel.get_all()
        try:
            output = articles_schema.dump(articles)
        except ValidationError as err:
            return err.messages, 422
        return output.data

    @jwt_needed
    def post(self):
        # Get json data, attach author id
        try:
            data = api.payload
            data['author_id'] = current_identity.id
        except:
            return ArticleInvalid.get_response()

        # validate data
        try:
            result = article_schema.load(data)
        except ValidationError as error:
            return ArticleInvalid.get_response(error=error.messages)

        # Good, save to db
        try:
            article = ArticleModel(**result.data)
            article.save()
        except CategoryNotFound as err:
            return CategoryNotFound.get_response()
        except:
            return ServerError.get_response()

        # Filter what should be showed to user
        output = article_schema.dump(article)

        # Send back
        return output.data


@api.route('/<article_id>')
class Article(Resource):
    @staticmethod
    def get(article_id):
        article = ArticleModel.find_by_id(article_id)
        if article is None:
            return ArticleNotFound.get_response()

        # Filter what should be showed to user
        output = article_schema.dump(article)

        # Send back
        return output.data

    @jwt_needed
    @must_be_author
    def delete(self, article_id):
        article = ArticleModel.find_by_id(article_id)
        try:
            article.delete()
        except:
            return ServerError.get_response()

        return {"message": "Successful deleted"}

    @jwt_needed
    @must_be_author
    def put(self, article_id):
        # Does article_id exist?
        article = ArticleModel.find_by_id(article_id)

        # Is data coming in good?
        try:
            data = api.payload
            data['author_id'] = current_identity.id
        except:
            return ArticleInvalid.get_response()

        try:
            result = article_schema.load(data)
        except ValidationError as error:
            return ArticleInvalid.get_response()

        # update to db
        try:
            article.update_props(**result.data)
            article.save()
        except CategoryNotFound:
            return CategoryNotFound.get_response()
        except:
            return ServerError.get_response()

        # Filter only what should be showed to user:
        output = article_schema.dump(article)

        # Good, successful
        return output.data
