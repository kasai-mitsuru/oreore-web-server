import datetime
import os

from application.henavel.controller.controller import Controller
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response, ResponseRedirect
from application.henavel.model.database import IN_MEMORY_DICT_DB
from application.henavel.view.view import View
from application.settings import TEMPLATES_DIR


class IndexController(Controller):
    def get(self, request: Request) -> Response:
        with open(os.path.join(TEMPLATES_DIR, "index.html")) as f:
            content = f.read()

        return Response(content=content)

    def post(self, request) -> Response:
        return Response()


class BBSController(Controller):
    def get(self, request: Request) -> Response:
        context = {"posts": IN_MEMORY_DICT_DB["posts"]}
        content = View("bbs.html", context).render()

        return Response(content=content)

    def post(self, request: Request) -> Response:
        post = {}
        post["name"] = request.POST["name"]
        post["body"] = request.POST["body"]
        post["created_at"] = datetime.datetime.now()

        IN_MEMORY_DICT_DB["posts"].append(post)

        return ResponseRedirect(location="/bbs")
