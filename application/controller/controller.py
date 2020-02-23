import datetime

from application.henavel.controller.controller import Controller
from application.henavel.controller.http.cookie import Cookie
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response, ResponseRedirect
from application.henavel.model.database import IN_MEMORY_DICT_DB
from application.henavel.view.view import View


class IndexController(Controller):
    def get(self, request: Request) -> Response:
        content = View("index.html").render()

        counter_cookie = None
        for cookie in request.cookies:
            if cookie.name == "counter":
                counter_cookie = cookie
            break

        if not counter_cookie:
            counter_cookie = Cookie(name="counter", value="0", max_age=300)
        else:
            counter_cookie.value = str(int(counter_cookie.value) + 1)
            counter_cookie.max_age = 300

        return Response(content=content, cookies=[counter_cookie])

    def post(self, request) -> Response:
        return Response()


class BBSController(Controller):
    def get(self, request: Request) -> Response:
        context = {"posts": IN_MEMORY_DICT_DB["posts"]}
        content = View("bbs.html", context).render()

        return Response(content=content)

    def post(self, request: Request) -> Response:
        post = {}
        post["name"] = request.POST["name"]
        post["body"] = request.POST["body"]
        post["created_at"] = datetime.datetime.now()

        IN_MEMORY_DICT_DB["posts"].append(post)

        return ResponseRedirect(location="/bbs")
