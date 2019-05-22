from db import db
from errors.user import UserAlreadyExists
from werkzeug.security import generate_password_hash


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def save(self):
        if self.find_by_username(self.username):
            raise UserAlreadyExists()
        else:
            db.session.add(self)
            db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        # return "User: {} | {} | {} | {}".format(self.username, self.first_name, self.last_name, self.password)
        return "User: {}".format(self.username)
