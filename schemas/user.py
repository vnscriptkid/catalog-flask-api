from marshmallow import Schema, fields, ValidationError, validates


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # password = fields.Str(required=True, load_only=True)
    # first_name = fields.Str(required=True)
    # last_name = fields.Str(required=True)
    # created_at = fields.DateTime(dump_only=True)

    # @validates('username')
    # def validate_username(self, username):
    #     if len(username) < 3 or len(username) > 20:
    #         raise ValidationError("Username must be in between 3 and 20 characters")

    # @validates('password')
    # def validate_password(self, password):
    #     if len(password) < 6 or len(password) > 15:
    #         raise ValidationError("Username must be in between 6 and 15 characters")
    #
    # @validates('first_name')
    # def validate_first_name(self, first_name):
    #     if len(first_name) < 3 or len(first_name) > 20:
    #         raise ValidationError("Firstname must be in between 3 and 20 characters")
    #
    # @validates('last_name')
    # def validate_first_name(self, last_name):
    #     if len(last_name) < 3 or len(last_name) > 20:
    #         raise ValidationError("Lastname must be in between 3 and 20 characters")

    class Meta:
        strict = True


user_schema = UserSchema()
