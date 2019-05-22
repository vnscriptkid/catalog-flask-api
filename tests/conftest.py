import pytest

from db import db
from app_factory import create_app
from models.category import CategoryModel
from models.user import UserModel
from models.article import ArticleModel


@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")

    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    cat_1 = CategoryModel("Travelling")
    cat_2 = CategoryModel("Book Review")
    user_1 = UserModel("vnscriptkid", "123456", "thanh", "nguyen")
    user_2 = UserModel("firmino123", "123456", "roberto", "firmino")
    art_1 = ArticleModel("first article", "content here", 1, 1)

    db.session.add(cat_1)
    db.session.add(cat_2)
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(art_1)

    db.session.commit()

    yield db

    db.drop_all()



