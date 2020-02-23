from typing import Dict


class Request:
    def __init__(self, env: Dict):
        self.method: str = env["REQUEST_METHOD"]
        self.path: str = env["PATH_INFO"]
        self.query: str = env["QUERY_STRING"]
        self.GET: Dict = {}
        self.POST: Dict = {}
        self.body: bytes = env["wsgi.input"]

        if self.query:
            self.GET = self.parse_query(self.query)

        if self.method == "POST":
            self.POST = self.parse_query(self.body.decode())

    @staticmethod
    def parse_query(query: str) -> Dict:
        if not query:
            return {}

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
