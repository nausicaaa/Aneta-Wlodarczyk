from databases import Database
from environs import Env
from sanic import Sanic
from sanic.response import json

from http_server.settings import Settings

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


def init():
    env = Env()
    env.read_env()

    config = app.config.from_object(Settings)

    setup_database()

    app.run(config)

