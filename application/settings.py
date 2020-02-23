import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

NOT_FOUND_FILE = os.path.join(TEMPLATES_DIR, "404.html")
