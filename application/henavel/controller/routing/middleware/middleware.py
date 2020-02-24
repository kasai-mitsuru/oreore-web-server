from abc import ABC

from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response
from application.henavel.controller.routing.route import Route


class Middleware(ABC):
    def wrap(self, route: Route) -> Route:
        current_api = route.get_response
        before_api = self.before
        after_api = self.after

        def wrapped_api(request: Request) -> Response:
            return after_api(current_api(before_api(request)))

        route.get_response = wrapped_api

        return route

    def before(self, request: Request) -> Request:
        return request

    def after(self, response: Response) -> Response:
        return response
