from abc import ABC, abstractmethod

from application.core.http.request import Request
from application.core.http.response import ResponseRedirect, Response


class BaseRouter(ABC):
    @abstractmethod
    def get_response(self, request: Request) -> Response:
        pass


class RouterView(BaseRouter):
    def __init__(self, view_class):
        self.view_class = view_class

    def get_response(self, request: Request) -> Response:
        return self.view_class().get_response(request)


class RouterRedirect(BaseRouter):
    def __init__(self, url: str):
        self.url = url

    def get_response(self, request: Request) -> ResponseRedirect:
        return ResponseRedirect(location=self.url)
