from marshmallow import Schema, fields, ValidationError, validates


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    @validates('name')
    def validate_name(self, name):
        if len(name) < 6:
            raise ValidationError("Length of 'name' must be greater than 5")

    class Meta:
        strict = True


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
