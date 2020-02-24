from abc import ABC, abstractmethod

from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response, ResponseRedirect


class Route(ABC):
    @abstractmethod
    def get_response(self, request: Request) -> Response:
        pass


class RouteController(Route):
    def __init__(self, controller_class):
        self.controller_class = controller_class

    def get_response(self, request: Request) -> Response:
        return self.controller_class().get_response(request)


class RouteRedirect(Route):
    def __init__(self, url: str):
        self.url = url

    def get_response(self, request: Request) -> ResponseRedirect:
        return ResponseRedirect(location=self.url)
