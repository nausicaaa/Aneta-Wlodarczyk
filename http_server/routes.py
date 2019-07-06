from sanic import response
from sanic.exceptions import InvalidUsage, NotFound, PayloadTooLarge
from sanic.response import json
from sqlalchemy import create_engine

from http_server import settings
from http_server.main import app
from http_server.tables import urls

engine = create_engine(settings.DB_URL)
connection = engine.connect()


@app.route("/api/fetcher/", methods=['POST'])
def post(request):
    if ['url', 'interval'] not in request.args:
        raise InvalidUsage('Incorrect json', status_code=400)

    if len(request.body) >= app.config.REQUEST_MAX_SIZE:
        raise PayloadTooLarge('Request too large', status_code=413)

    url = request.args['url']
    interval = request.args['interval']
    insert_query = urls.insert().values(
        url=url, interval=interval, response=response)
    result = insert_query.execute()
    return json({'id': result.inserted_primary_key})


