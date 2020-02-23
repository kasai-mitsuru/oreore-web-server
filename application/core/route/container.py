import os
from importlib import import_module
from pathlib import Path
from typing import Dict

from application.core.route.router import BaseRouter, RouterView, RouterRedirect
from application.settings import ROUTES_DIR, BASE_DIR


class Container:
    def __init__(self):
        self.container: Dict[str, BaseRouter] = {}

    def is_registered(self, route: str):
        return route in self.container

    def resolve(self, route: str):
        if route not in self.container:
            raise RouterNotRegisteredError(f"a router for '{route}' is not found.")
        return self.container[route]

    def view(self, route: str, view_class):
        self.container[route] = RouterView(view_class)

    def redirect(self, route: str, url: str):
        self.container[route] = RouterRedirect(url)


class RouterNotRegisteredError(Exception):
    pass


def import_routes():
    route_files = Path(ROUTES_DIR).glob("*.py")

    for file in route_files:
        module_name = file.name.rsplit(".py")[0]
        import_module(f"application.routes.{module_name}")


route_container = Container()
import_routes()
