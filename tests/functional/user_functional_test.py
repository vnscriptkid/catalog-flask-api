from flask import json


def test_auth(test_client, init_database):
    res = test_client.post('/auth', json=dict(
        username="vnscriptkid",
        password="123456"
    ))
    assert res.status_code == 200
    json_data = json.loads(res.data)
    assert "access_token" in json_data


def test_falsy_credentials(test_client, init_database):
    res = test_client.post('/auth', json=dict(
        username="fakeusername",
        password="fakepass"
    ))
    json_data = json.loads(res.data)
    assert res.status_code == 401
    assert json_data['description'] == 'Invalid credentials'

