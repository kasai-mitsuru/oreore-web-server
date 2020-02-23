from typing import Dict, List
from urllib.parse import unquote

from application.henavel.controller.http.cookie import Cookie


class Request:
    def __init__(self, env: Dict):
        self.method: str = env["REQUEST_METHOD"]
        self.path: str = env["PATH_INFO"]
        self.query: str = env["QUERY_STRING"]
        self.GET: Dict = {}
        self.POST: Dict = {}
        self.cookies: List[Cookie] = []
        self.body: bytes = env["wsgi.input"].read()

        if self.query:
            self.GET = self.parse_query(self.query)

        if self.method == "POST":
            self.POST = self.parse_query(self.body.decode())

        if "HTTP_COOKIE" in env:
            self.cookies = self.build_cookies(env["HTTP_COOKIE"])

    @staticmethod
    def parse_query(query: str) -> Dict:
        if not query:
            return {}

        query = unquote(query)

        param_strings = query.split("&")
        params = {}
        for param_string in param_strings:
            splitted = param_string.split("=", 1)
            if len(splitted) == 1:
                key, value = splitted[0], ""
            else:
                key, value = splitted[0], splitted[1]

            params[key] = value

        return params

    @staticmethod
    def build_cookies(line: str) -> List[Cookie]:
        cookies = []
        pairs = line.split(";")

        for pair in pairs:
            name, value = pair.strip().split("=", 1)
            cookies.append(Cookie(name=name, value=value))

        return cookies
