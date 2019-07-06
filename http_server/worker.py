from sanic import response
from sanic.response import text, json

from http_server.main import app
from http_server.routes import save_data_to_db

MAXSIZE = 10

# TODO: Add interval in seconds to fetch url by worker

@app.get("/api/fetcher", method=['GET'])
async def add_to_queue(request, queue):
    try:
        await queue.put_nowait(request, timeout=5)
    except Exception as e:
        save_data_to_db(request)
        return text(f"Something went wrong for  url: {request.url}, {str(e)}")

    return json(response)

async def fetch_urls_worker(app, queue):
    while True:
        job = await queue.get(timeout=5)
        print((f"{job} is running."))
