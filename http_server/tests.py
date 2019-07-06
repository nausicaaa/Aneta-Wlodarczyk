from http_server.main import app


def test_post():
    data = {"url": "url3", "interval": 15}
    request, response = app.test_client.post('/api/fetcher', data=json.dumps(data))
    assert response.json.get('id') == 3
    assert response.json.get('url') == 'url1'
    assert response.json.get('interval') == 15


def test_post_400_exception():
    request, response = app.test_client.post("/api/fetcher", data=invalid_json)
    assert response.status == 400


def test_post_413_exception():
    request, response = app.test_client.post("/api/fetcher", data=open("test_file_1mb.txt", 'rb'))
    assert response.status == 413

