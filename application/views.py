import os
from abc import ABC

from application.core.http.request import Request
from application.core.http.response import Response, ResponseBadRequest
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


class IndexView(BaseView):
    def get(self, request: Request) -> Response:
        with open(os.path.join(TEMPLATES_DIR, "index.html")) as f:
            content = f.read()

        return Response(content=content)

    def post(self, request) -> Response:
        return Response()


class SampleFormView(BaseView):
    pass
