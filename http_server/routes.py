from sanic import response
from sanic.exceptions import InvalidUsage, NotFound, PayloadTooLarge
from sanic.response import json
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound

from http_server import settings
from http_server.main import app
from http_server.tables import urls

#TODO: Use Session object for db connection would be more effective
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

@app.route("/api/fetcher", methods=['GET'])
def get(request):
    query = urls.select()
    rows = request.app.db.fetch_all(query)
    return [
        {'id': row['id'],
         'url': row['url'],
         'interval': row['interval']}
        for row in rows
    ]

@app.route("/api/fetcher/<id>/history", methods=['GET'])
def get_url(request, id):
    try:
        int(id)
    except ValueError:
        raise InvalidUsage('Incorrect id format provided', status_code=400)

    query = urls.select(urls).where(urls.c.id == id)
    try:
        rows = request.app.db.fetch_all(query)
    except NoResultFound:
        raise NotFound('Result not found', status_code=404)

    return [
        {'response': row['response'],
         'created_at': row['created_at']}
        for row in rows
    ]

@app.route("/api/fetcher/<id>", methods=['DELETE'])
def delete(request, id):
    query = urls.delete().where(urls.c.id == id)
    query.execute()
    return json({'id': id})


