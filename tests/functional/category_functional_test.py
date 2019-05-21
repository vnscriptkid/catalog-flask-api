def test_get_categories(test_client):
    res = test_client.get('/categories')
    assert res.status_code == 200
