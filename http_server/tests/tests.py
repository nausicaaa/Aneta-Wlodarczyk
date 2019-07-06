import json

from http_server.main import app


def test_app():
    _, response = app.test_client.get("/")
    assert response.status == 200

#TODO: Instead of patching db connection pytest fixtures should be used for testing
# I created initial draft of pytest fixture for SQLAlchem in conftest.py

class TestRoutesClass:
    @classmethod
    def setup_class(cls):
        data = [{"url": "url1", "interval": 60}, {"url": "url2", "interval": 5}]
        for _ in data:
            app.test_client.post('/api/fetcher', data=json.dumps(_))

    def test_post(self):
        data = {"url": "url3", "interval": 15}
        request, response = app.test_client.post('/api/fetcher', data=json.dumps(data))
        assert response.json.get('id') == 3
        assert response.json.get('url') == 'url1'
        assert response.json.get('interval') == 15


    def test_post_400_exception(self):
        request, response = app.test_client.post("/api/fetcher", data=invalid_json)
        assert response.status == 400

    def test_post_413_exception(self):
        request, response = app.test_client.post("/api/fetcher", data=open("test_file_1mb.txt", 'rb'))
        assert response.status == 413

    def test_get(self):
        request, response = app.test_client.get('/api/fetcher')
        assert len(response) == 2

    def test_get_url(self):
        request, response = app.test_client.get_url('/api/fetcher/1/history')
        assert len(response) == 1
        assert 'response' in response[0].keys()

    def test_get_400_exception(self):
        invalid_id = "invalid_id"
        request, response = app.test_client.get_url(f"/api/fetcher/{invalid_id}/history")
        assert response.status == 400

    def test_get_404_exception():
        not_existing_id = 1000000
        request, response = app.test_client.get_url(f"/api/fetcher/{not_existing_id}/history")
        assert response.status == 404

    def test_delete(self):
        data = [{"url": "url1", "interval": 60}, {"url": "url2", "interval": 5}]
        for _ in data:
            app.test_client.post('/api/fetcher', data=json.dumps(_))
        request, response = app.test_client.delete("/api/fetcher/1")
        # TODO: check if delete() and execute() where called
        assert response.json.get('id') == 1

# TODO: add tests for workers

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