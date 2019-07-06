from environs import Env
from sanic import Sanic
from sanic.response import json
from http_server.settings import Settings

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})

def init():
    env = Env()
    env.read_env()
    config = app.config.from_object(Settings)

    app.run(config)

