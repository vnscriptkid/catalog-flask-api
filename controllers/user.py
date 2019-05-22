from flask_restplus import Resource, Namespace
from marshmallow import ValidationError

from schemas.user import user_schema
from models.user import UserModel
from errors.user import UserAlreadyExists

api = Namespace('users', description="User operations")


@api.route('/')
class Users(Resource):
    @staticmethod
    def post():
        # Parse request
        try:
            data = api.payload
        except:
            return {'message': 'Bad request'}, 400

        # Is data coming in good?
        try:
            result = user_schema.load(data)
        except ValidationError as error:
            return error.messages, 422

        # Good, save to db
        try:
            user = UserModel(**result.data)
            user.save()
        except UserAlreadyExists as err:
            return {'message': err.message}, 409
        except:
            return {'message': 'Can not create new user'}, 500

        # Is data coming out good?
        try:
            output = user_schema.dump(user)
        except ValidationError as err:
            return err.messages, 422

        # Good, successful
        return output.data, 201
