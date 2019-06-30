import json

import requests
from sanic import Sanic
from sanic.response import json as sanic_json, text
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage, PayloadTooLarge, ServerError, SanicException

app = Sanic()

@app.route("/")
async def test(request):
    return sanic_json({"hello": "world"})


class SimpleView(HTTPMethodView):

  # def get(self, request):
  #     return text('I am get method')


  def post(self, request):
      try:
          json.loads(request)
      except InvalidUsage as e:
          return text(e, e.status_code)
      # except PayloadTooLarge as e:
      #     return text(e, e.status_code)
      return sanic_json({ "id": 1})


app.add_route(SimpleView.as_view(), "/api/fetcher")
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)