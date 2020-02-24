from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response
from application.henavel.controller.routing.middleware.middleware import Middleware


class SampleMiddleware(Middleware):
    def before(self, request: Request) -> Request:
        return request

    def after(self, response: Response) -> Response:
        return response
