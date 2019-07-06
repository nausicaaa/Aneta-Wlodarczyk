import asyncio

from databases import Database
from environs import Env
from sanic import Sanic
from sanic.response import json
from sqlalchemy import create_engine, MetaData, Table

from http_server import worker, settings
from http_server.settings import Settings
from http_server.tables import urls

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})

def setup_database():
    app.db = Database(app.config.DB_URL)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.db.disconnect()

#TODO: Can be done manually when setting up environment and put in README
@app.listener('after_server_start')
def create_table_if_not_exists():
    engine = create_engine(settings.DB_URI)
    if not engine.has_table(engine, 'urls'):
        metadata = MetaData(engine)
        metadata.create_all(tables=urls)

def init():
    env = Env()
    env.read_env()

    # probably I should use here app.create_server method
    config = app.config.from_object(Settings)

    setup_database()
    create_table_if_not_exists()

    app.run(config)

