from flask import json


def test_get_articles(test_client, init_database):
    res = test_client.get('/articles')
    assert res.status_code == 200
    assert len(json.loads(res.data)) == 0


def test_post_article_without_token(test_client, init_database):
    res = test_client.post('/articles')
    json_data = json.loads(res.data)
    assert  res.status_code == 499
    assert json_data['Authorization Required'] == 'Request does not contain an access token'


def test_post_article_with_valid_token(test_client, init_database):
    # Get token first
    res = test_client.post('/auth', json=dict(
        username="vnscriptkid",
        password="123456"
    ))
    assert res.status_code == 200
    json_data = json.loads(res.data)
    assert "access_token" in json_data
    # Post article with token
    art = {
        "title": "heading",
        "body": "content",
        "category_id": 2
    }
    res = test_client.post(
        '/articles',
        headers={'Authorization': "JWT {}".format(json_data['access_token'])},
        json=art
    )
    json_article = json.loads(res.data)
    assert res.status_code == 201
    assert json_article['title'] == art['title']
    assert json_article['body'] == art['body']
    assert json_article['category']['id'] == 2
    assert json_article['author']['username'] == "vnscriptkid"
    assert json_article['id'] == 1
    assert "created_at" in json_article
    assert "modified_at" in json_article


def test_delete_article_without_token(test_client, init_database):
    res = test_client.delete('/articles/1')
    json_data = json.loads(res.data)
    assert res.status_code == 499
    assert json_data['Authorization Required'] == 'Request does not contain an access token'


def test_edit_article_without_token(test_client, init_database):
    res = test_client.put('/articles/1')
    json_data = json.loads(res.data)
    assert res.status_code == 499
    assert json_data['Authorization Required'] == 'Request does not contain an access token'
