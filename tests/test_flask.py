from app import app

import os
import tempfile

import pytest

from app_factory import create_app


@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

    with flaskr.app.app_context():
        flaskr.init_db()

    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


def test_homepage():
    res = app.test_client().get('/')
    assert res.status_code == 200
