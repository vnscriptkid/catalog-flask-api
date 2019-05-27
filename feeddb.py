from sqlalchemy import create_engine
engine = create_engine('sqlite:///db.sqlite.prod', echo=True)
from sqlalchemy.orm import sessionmaker
from models.user import UserModel
from models.category import CategoryModel
from models.article import ArticleModel
from app_factory import create_app
from db import db
from random import randint, choice
import string

Session = sessionmaker(bind=engine)
session = Session()

app = create_app("development")
db.create_all(app=app)


# Feed users
session.add_all([
    UserModel(username="vnscriptkid", password="123456", first_name="thanh", last_name="nguyen"),
    UserModel(username="firmino9", password="123456", first_name="roberto", last_name="firmino"),
    UserModel(username="hendo14", password="123456", first_name="jordan", last_name="henderson"),
    UserModel(username="mane10", password="123456", first_name="sadio", last_name="mane"),
    UserModel(username="mosalah11", password="123456", first_name="mohamed", last_name="salah"),
    UserModel(username="keita8", password="123456", first_name="naby", last_name="keita")
])

# Feed Categories
session.add_all([
    CategoryModel(name="Shopping"),
    CategoryModel(name="Travelling"),
    CategoryModel(name="Coding"),
    CategoryModel(name="Cuisine"),
    CategoryModel(name="Football"),
    CategoryModel(name="Celebrities"),
    CategoryModel(name="Scandal"),
    CategoryModel(name="News"),
    CategoryModel(name="Gym"),
    CategoryModel(name="Love"),
])


# Feed Articles
def random_word():
    random_length = randint(3, 6)
    result = ""
    while len(result) < random_length:
        token = choice(string.ascii_lowercase)
        result += token
    return result


def random_text(min_length, max_length):
    num_of_words = randint(min_length, max_length)
    result = ""
    count = 0
    while count < num_of_words:
        added = random_word()
        if count > 0:
            added = " " + added
        result += added
        count += 1
    return result


def random_article():
    return ArticleModel(
        title=random_text(5, 10),
        body=random_text(100, 200),
        category_id=randint(1, 10),
        author_id=randint(1, 6)
    )


session.add_all([random_article() for x in range(200)])

session.commit()
