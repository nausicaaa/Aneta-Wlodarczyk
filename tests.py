import json
from main import app


def test_get():
    _, response = app.test_client.get("/")
    assert response.status == 200

def test_post_json_request():
    data = {"url": "url", "interval": 60}
    request, response = app.test_client.post('/api/fetcher', data=json.dumps(data))
    print(response.json)
    assert response.json.get('id') == 1


def test_invalid_usage_exception():
    request, response = app.test_client.post("/api/fetcher", json=None)
    assert response.status == 400
