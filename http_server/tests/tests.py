import json

import mock

from http_server.main import app




def test_app():
    _, response = app.test_client.get("/")
    assert response.status == 200

#TODO: Instead of patching db connection pytest fixtures should be used for testing

@mock.patch('app.http_server.routes.create_engine')
def test_post():
    data = {"url": "url1", "interval": 60}
    request, response = app.test_client.post('/api/fetcher', data=json.dumps(data))
    # to trzeba zamockować żeby 1 da i sprawdzic czy execute mock albo insert sie wykonal
    assert response.json.get('id') == 1
    assert response.json.get('url') == 'url1'
    assert response.json.get('interval') == 60


def test_post_400_exception():
    request, response = app.test_client.post("/api/fetcher", data=invalid_json)
    assert response.status == 400

def test_post_413_exception():
    request, response = app.test_client.post("/api/fetcher", data=open("test_file_1mb.txt", 'rb'))
    assert response.status == 413

def test_get():
    # populate db
    #TODO: Should be fixture with populated db or a factory
    data = [{"url": "url1", "interval": 60}, {"url": "url2", "interval": 5}]
    for _ in data:
        app.test_client.post('/api/fetcher', data=json.dumps(_))

    request, response = app.test_client.get('/api/fetcher')
    assert len(response) == 2

def test_get_url():
    # populate db przenieś to wyżej
    #TODO: Should be fixture with populated db or a factory
    data = [{"url": "url1", "interval": 60}, {"url": "url2", "interval": 5}]
    for _ in data:
        app.test_client.post('/api/fetcher', data=json.dumps(_))

    request, response = app.test_client.get_url('/api/fetcher/1/history')
    assert len(response) == 1
    # powinnam zamockować bazę w tak sposob, zeby byly tam już zapisane reponses jakies
    assert 'response' in response[0].keys()

def test_get_400_exception():
    invalid_id = "invalid_id"
    request, response = app.test_client.get_url(f"/api/fetcher/{invalid_id}/history")
    assert response.status == 400

def test_get_404_exception():
    not_existing_id = 1000000
    request, response = app.test_client.get_url(f"/api/fetcher/{not_existing_id}/history")
    assert response.status == 404

def test_delete():
    data = [{"url": "url1", "interval": 60}, {"url": "url2", "interval": 5}]
    for _ in data:
        app.test_client.post('/api/fetcher', data=json.dumps(_))
    request, response = app.test_client.delete("/api/fetcher/1")
    # TODO: check if delete() and execute() where called
    assert response.json.get('id') == 1

invalid_json = """{
    {
    "actor": [
      {
        "firstName": "Tom",
        "lastName": "Cruise"
      }
    ]
  }
}
 """