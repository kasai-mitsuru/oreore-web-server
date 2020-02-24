import sys
from importlib import import_module
from pathlib import Path
from typing import Dict

from application.henavel.controller.http.cookie import Cookie
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response
from application.henavel.controller.middlewares.session_middleware import (
    SessionIDGenerator,
)
from application.henavel.controller.routing.route import (
    RouteController,
    RouteRedirect,
    BaseRoute,
)
from application.settings import ROUTES_DIR


class SessionMiddleware(BaseRoute):
    SESSION_ID_NAME = "HENASESSION_ID"
    SESSION_LIFETIME = 5

    def __init__(self, route: BaseRoute):
        self.route: BaseRoute = route

    def get_response(self, request: Request) -> Response:
        current_cookie = request.cookies.get(self.SESSION_ID_NAME)

        if current_cookie is None:
            session_id = SessionIDGenerator().generate()
        else:
            session_id = current_cookie.value

        next_cookie = Cookie(
            self.SESSION_ID_NAME, session_id, max_age=self.SESSION_LIFETIME
        )

        response = self.route.get_response(request)

        response.cookies.save(next_cookie)

        return response


class RouteContainer:
    def __init__(self):
        self.container: Dict[str, BaseRoute] = {}

    def is_registered(self, route: str):
        return route in self.container

    def resolve(self, path: str) -> BaseRoute:
        if path not in self.container:
            raise RouteNotRegisteredError(f"a route for '{path}' is not found.")

        route = self.container[path]

        route = SessionMiddleware(route)

        return route

    def controller(self, route: str, controller_class):
        self.container[route] = RouteController(controller_class)

    def redirect(self, route: str, url: str):
        self.container[route] = RouteRedirect(url)


class RouteNotRegisteredError(Exception):
    pass


def import_routes():
    sys.path.append(ROUTES_DIR)
    route_files = Path(ROUTES_DIR).glob("*.py")

    for file in route_files:
        module_name = file.name.rsplit(".py")[0]
        import_module(f"{module_name}")

    sys.path.pop()


route_container = RouteContainer()
import_routes()
