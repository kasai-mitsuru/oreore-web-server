import datetime
import os

from application.henavel.controller.controller import Controller
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response, ResponseRedirect
from application.henavel.model.database import IN_MEMORY_DICT_DB
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
        content = self.render("bbs.html", {"posts": IN_MEMORY_DICT_DB["posts"]})

        return Response(content=content)

    def post(self, request: Request) -> Response:
        post = {}
        post["name"] = request.POST["name"]
        post["body"] = request.POST["body"]
        post["created_at"] = datetime.date.today()

        IN_MEMORY_DICT_DB["posts"].append(post)

        return ResponseRedirect(location="/bbs")
