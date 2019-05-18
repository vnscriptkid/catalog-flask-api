from marshmallow import Schema, fields

from schemas.category import CategorySchema


class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    category = fields.Nested(CategorySchema, required=True, dump_only=True)
    category_id = fields.Int(load_only=True, required=True)

    class Meta:
        strict = True


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
