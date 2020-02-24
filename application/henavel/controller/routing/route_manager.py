import sys
from importlib import import_module
from pathlib import Path
from typing import Dict

from application.henavel.controller.routing.middleware.container import (
    middleware_manager,
)
from application.henavel.controller.routing.route import (
    RouteController,
    RouteRedirect,
    Route,
)
from application.settings import ROUTES_DIR


class RouteManager:
    def __init__(self):
        self.container: Dict[str, Route] = {}

    def is_registered(self, route: str):
        return route in self.container

    def resolve(self, path: str) -> Route:
        if path not in self.container:
            raise RouteNotRegisteredError(f"a route for '{path}' is not found.")

        route = self.container[path]

        route = middleware_manager.wrap(route)

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
        if file.name == "__init__.py":
            continue

        module_name = file.name.rsplit(".py", 1)[0]
        import_module(f"{module_name}")

    sys.path.pop()


route_manager = RouteManager()
import_routes()
