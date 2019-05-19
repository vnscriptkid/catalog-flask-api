from flask_restplus import Resource, Namespace
from flask import request
from marshmallow import ValidationError

from schemas.user import user_schema
from models.user import UserModel
from errors.user import UserAlreadyExists


# class UserRegister(Resource):
#     def post(self):
#         try:
#             data = request.get_json()
#         except:
#             return {'msg': 'Bad request'}
#         try:
#             result = user_schema.load(data)
#         except ValidationError as error:
#             return error.messages, 422
#
#             return {'msg': 'Username already exists'}, 400
#
#         try:
#             new_user = UserModel(**result.data)
#             new_user.save()
#             print(new_user)
#         except ReferenceError as err:
#             return err.args, 409
#         except:
#             return {'msg': 'Can not create new user'}, 500
#
#         return result.data, 201

api = Namespace('users', description="Users operations")


@api.route('/register')
class UserRegister(Resource):
    @staticmethod
    def post():
        try:
            # data = request.get_json()
            data = api.payload
        except:
            return {'msg': 'Bad request'}
        try:
            result = user_schema.load(data)
        except ValidationError as error:
            return error.messages, 422

            # return {'msg': 'Username already exists'}, 400

        # try:
            new_user = UserModel(result.data['username'])
            print(new_user)
            new_user.save()
        # except UserAlreadyExists as err:
        #     return err.args, 409
        # except:
        #     return {'msg': 'Can not create new user'}, 500

        return result.data, 201

