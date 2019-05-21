from flask import json

DEFAULT_USER = {
    "username": "vnscriptkid",
    "password": "123456"
}

SECOND_USER = {
    "username": "firmino123",
    "password": "123456"
}


def get_token_helper(test_client, user=DEFAULT_USER):
    res = test_client.post('/auth', json=user)
    json_data = json.loads(res.data)
    assert res.status_code == 200
    assert "access_token" in json_data
    print(json_data['access_token'])
    return json_data['access_token']


def test_get_articles(test_client, init_database):
    res = test_client.get('/articles')
    assert res.status_code == 200
    assert len(json.loads(res.data)) == 1


def test_post_article_without_token(test_client, init_database):
    res = test_client.post('/articles')
    json_data = json.loads(res.data)
    assert res.status_code == 499
    assert json_data['Authorization Required'] == 'Request does not contain an access token'


def test_post_article_with_valid_token(test_client, init_database):
    # Get token first
    token = get_token_helper(test_client)
    # Post article with token
    art = {
        "title": "heading",
        "body": "content",
        "category_id": 2
    }
    res = test_client.post(
        '/articles',
        headers={'Authorization': "JWT {}".format(token)},
        json=art
    )
    json_article = json.loads(res.data)
    assert res.status_code == 201
    assert json_article['title'] == art['title']
    assert json_article['body'] == art['body']
    assert json_article['category']['id'] == 2
    assert json_article['author']['username'] == "vnscriptkid"
    assert json_article['id'] == 2
    assert "created_at" in json_article
    assert "modified_at" in json_article


def test_delete_article_without_token(test_client, init_database):
    res = test_client.delete('/articles/1')
    json_data = json.loads(res.data)
    assert res.status_code == 499
    assert json_data['Authorization Required'] == 'Request does not contain an access token'


def test_delete_article_with_valid_token_by_author(test_client, init_database):
    # Get token first
    token = get_token_helper(test_client)

    # Delete first article
    res = test_client.delete('/articles/1', headers={'Authorization': "JWT {}".format(token)})

    assert res.status_code == 204


def test_delete_article_with_valid_token_not_by_author(test_client, init_database):
    # Get token first
    token = get_token_helper(test_client, user=SECOND_USER)

    # Delete first article
    res = test_client.delete('/articles/2', headers={'Authorization': "JWT {}".format(token)})

    assert res.status_code == 401
    json_data = json.loads(res.data)
    assert json_data['msg'] == 'Unauthorized access'


def test_edit_article_without_token(test_client, init_database):
    res = test_client.put('/articles/1')
    json_data = json.loads(res.data)
    assert res.status_code == 499
    assert json_data['Authorization Required'] == 'Request does not contain an access token'
