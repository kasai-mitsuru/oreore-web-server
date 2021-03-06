import datetime
import os
from typing import Dict, Callable, List, Tuple, Iterable

from application.henavel.controller.http.consts import (
    STATUS_SERVER_ERROR,
    REASON_PHRASES,
)
from application.henavel.controller.http.cookie import CookieContainer
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import ResponseNotFound, Response
from application.henavel.controller.routing.route_manager import route_manager
from application.settings import PUBLIC_DIR


class WSGIApplication:
    def __call__(
        self, env: Dict, start_response: Callable[[str, List[Tuple[str, str]]], None]
    ) -> Iterable[bytes]:

        request = Request(env)

        path = request.path
        if route_manager.is_registered(path):
            # 登録済みのrouteからレスポンスを取得する
            route = route_manager.resolve(path)
            response = route.get_response(request)
        else:
            # routeに登録されていなかった場合、静的ファイルを取得しにいく
            relative_path = request.path.split(os.sep, 1)[1]
            path = os.path.join(PUBLIC_DIR, relative_path)

            if not os.path.exists(path):
                # 静的ファイルもない場合はNot Foundとする
                response = ResponseNotFound()
            else:
                with open(path, "rb") as f:
                    content = f.read()
                content_type = self.get_mime_type(path)
                response = Response(content=content, content_type=content_type)

        status_line = self.get_status_line(response)
        headers = self.get_headers(response)
        content = self.get_content(response)

        start_response(status_line, headers)
        return [content]

    @staticmethod
    def get_mime_type(path: str) -> str:
        file_name = os.path.basename(path)
        ext = file_name.rsplit(".")[1] if file_name.find(".") else ""

        return {
            "txt": "text/plain",
            "html": "text/html",
            "css": "text/css",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
        }.get(ext.lower(), "application/octet-stream")

    @staticmethod
    def get_status_line(response) -> str:
        status_code = getattr(response, "status_code", 0)
        status_code = status_code if status_code else STATUS_SERVER_ERROR
        reason_phrase = getattr(response, "response_phrase", "")
        reason_phrase = reason_phrase if reason_phrase else REASON_PHRASES[status_code]
        status_line = f"{str(status_code)} {reason_phrase}"

        return status_line

    @staticmethod
    def get_headers(response) -> List[Tuple[str, str]]:
        content_type = getattr(response, "content_type", "")
        content_type = content_type if content_type else "text/html"

        headers = [
            ("Date", datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            ("Server", "Henacorn v0.1"),
            ("Connection", "Close"),
            ("Content-Type", content_type),
        ]

        location = getattr(response, "location", "")
        if location:
            headers.append(("Location", location))

        cookies: CookieContainer = getattr(response, "cookies", [])
        for cookie in cookies:
            headers.append(("Set-Cookie", cookie.get_header_format()))

        return headers

    @staticmethod
    def get_content(response: Response) -> bytes:
        content = getattr(response, "content", b"")
        if isinstance(content, str):
            content = content.encode()

        return content
