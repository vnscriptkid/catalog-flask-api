from db import db
from models.category import CategoryModel
from errors.category import CategoryNotFound


class ArticleModel(db.Model):

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('CategoryModel', backref=db.backref('articles', lazy=True))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('UserModel', backref=db.backref('articles', lazy=True))

    def __init__(self, title, body, category_id, author_id):
        self.title = title
        self.body = body
        self.category_id = category_id
        self.author_id = author_id

    def save(self):
        cat = CategoryModel.find_by_id(self.category_id)
        if cat is None:
            raise CategoryNotFound()
        else:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_cat(cls, cat):
        return cls.query.with_parent(cat).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def update_props(self, title, body, category_id):
        self.title = title
        self.body = body
        self.category_id = category_id

    def __repr__(self):
        return "Article: {}, {}, {}".format(self.title, self.body, self.category_id)