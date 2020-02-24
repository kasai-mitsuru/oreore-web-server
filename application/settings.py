import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "view", "templates")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
ROUTES_DIR = os.path.join(BASE_DIR, "controller", "routes")

NOT_FOUND_FILE = os.path.join(TEMPLATES_DIR, "404.html")

MIDDLEWARES = [
    "application.henavel.controller.middlewares.session_middleware.SessionMiddleware"
]
