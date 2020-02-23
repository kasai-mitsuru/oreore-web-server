import datetime
import os
from abc import ABC

from jinja2 import Environment, FileSystemLoader

from application.core.database import IN_MEMORY_LIST_DB
from application.core.http.request import Request
from application.core.http.response import (
    Response,
    ResponseBadRequest,
    ResponseRedirect,
)
from application.settings import TEMPLATES_DIR


class BaseView(ABC):
    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            response = self.get(request)
        elif request.method == "POST":
            response = self.post(request)
        else:
            raise

        return response

    def get(self, request: Request) -> Response:
        return ResponseBadRequest()

    def post(self, request: Request) -> Response:
        return ResponseBadRequest()

    @staticmethod
    def render(template_name: str, context=None):
        if context is None:
            context = {}
        template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = template_env.get_template(template_name)
        content = template.render(context)

        return content


class IndexView(BaseView):
    def get(self, request: Request) -> Response:
        with open(os.path.join(TEMPLATES_DIR, "index.html")) as f:
            content = f.read()

        return Response(content=content)

    def post(self, request) -> Response:
        return Response()


class BBSView(BaseView):
    def get(self, request: Request) -> Response:
        content = self.render("bbs.html", {"posts": IN_MEMORY_LIST_DB["posts"]})

        return Response(content=content)

    def post(self, request: Request) -> Response:
        post = {}
        post["name"] = request.POST["name"]
        post["body"] = request.POST["body"]
        post["created_at"] = datetime.date.today()

        IN_MEMORY_LIST_DB["posts"].append(post)

        return ResponseRedirect(location="/bbs")
