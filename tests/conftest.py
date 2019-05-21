import pytest

from db import db
from app_factory import create_app
from models.category import CategoryModel


@pytest.fixture(scope="module")
def test_client():
    """Create and configure a new app instance for each test."""
    app = create_app("testing")

    testing_client = app.test_client()

    # setup_db(app)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


def setup_db(app):
    db.init_app(app)

    cat_1 = CategoryModel("Travelling")
    cat_2 = CategoryModel("Book Review")

    db.session.add(cat_1)
    db.session.add(cat_2)

    db.session.commit()
