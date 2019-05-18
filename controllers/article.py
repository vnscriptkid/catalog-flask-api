from flask_restplus import Namespace, Resource
from marshmallow import ValidationError
from schemas.article import article_schema, articles_schema
from models.article import ArticleModel
from models.category import CategoryModel

api = Namespace('articles', description="Article operations")


@api.route('/')
class ArticleList(Resource):
    def get(self):
        arts = ArticleModel.get_all()
        try:
            output = articles_schema.dump(arts)
        except ValidationError as err:
            return err.messages, 422
        return output.data, 200

    def post(self):
        try:
            data = api.payload
        except:
            return {'msg': 'Bad Request'}, 400

        try:
            result = article_schema.load(data)
        except ValidationError as err:
            return err.messages, 422

        try:
            art = ArticleModel(**result.data)
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


@api.route('/<_id>')
class Article(Resource):
    def get(self, _id):
        art = ArticleModel.find_by_id(_id)
        if art is None:
            return {'msg': 'Article not found'}, 404
        cat = CategoryModel.find_by_id(art.category_id)
        art.category = cat
        try:
            output = article_schema.dump(art)
        except ValidationError as err:
            return err.messages, 422

        return output.data, 200

    def delete(self, _id):
        art = ArticleModel.find_by_id(_id)
        if art is None:
            return {'msg': 'Article not found'}, 404
        try:
            art.delete()
        except:
            return {'msg': 'Can not delete the article'}, 500
        return {'success': True, 'msg': 'The article has been deleted'}, 200

    def update(self, _id):
        art = ArticleModel.find_by_id(_id)
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






