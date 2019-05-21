from flask import json


def test_get_categories(test_client, init_database):
    print('init db', init_database)
    res = test_client.get('/categories')
    assert res.status_code == 200
    assert len(json.loads(res.data)) == 2
