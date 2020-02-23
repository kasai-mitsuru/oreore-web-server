from abc import ABC

from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response, ResponseBadRequest


class Controller(ABC):
    def get_response(self, request: Request) -> Response:
        if request.method == "GET":
            response = self.get(request)
        elif request.method == "POST":
            response = self.post(request)
        else:
            raise

        return response

    def get(self, request: Request) -> ResponseBadRequest:
        return ResponseBadRequest()

    def post(self, request: Request) -> ResponseBadRequest:
        return ResponseBadRequest()
