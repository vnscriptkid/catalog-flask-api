from db import db
from errors.category import CategoryAlreadyExists


class CategoryModel(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        if self.find_by_name(self.name):
            raise CategoryAlreadyExists()
        else:
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "Category: {}".format(self.name)