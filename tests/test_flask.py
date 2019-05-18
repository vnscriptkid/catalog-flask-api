from app import app
from flask import json


def test_homepage():
    res = app.test_client().get('/')
    json_data = res.get_json()
    assert json_data['msg'] == 'Homepage works well!'
    assert res.status_code == 200
