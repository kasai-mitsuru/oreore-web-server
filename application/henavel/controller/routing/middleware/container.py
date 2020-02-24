from importlib import import_module
from typing import List

from application import settings
from application.henavel.controller.routing.middleware.middleware import Middleware
from application.henavel.controller.routing.route import Route


class MiddlewareContainer(Middleware):
    def __init__(self):
        self.middlewares: List[Middleware] = self.correct_middlewares()

    def wrap(self, route: Route) -> Route:
        for middleware in reversed(self.middlewares):
            route = middleware.wrap(route)

        return route

    @staticmethod
    def correct_middlewares() -> List[Middleware]:
        middleware_names = settings.MIDDLEWARES
        middlewares = []
        for name in middleware_names:
            module, class_name = name.rsplit(".", 1)
            module = import_module(module)
            middleware = getattr(module, class_name)()
            middlewares.append(middleware)

        return middlewares


middleware_container = MiddlewareContainer()
