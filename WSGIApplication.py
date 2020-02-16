import datetime
import logging
import os
from typing import Dict, Callable, List, Tuple, Iterable

from consts import STATUS_OK, NOT_FOUND_DOCUMENT, STATUS_NOT_FOUND, HTTP_STATUS_MESSAGE
from env import DOCUMENT_ROOT


class WSGIApplication:
    def __call__(
        self, env: Dict, start_response: Callable[[str, List[Tuple[str, str]]], None]
    ) -> Iterable[bytes]:
        path = DOCUMENT_ROOT + env.get("PATH_INFO")

        try:
            with open(path, "br") as f:
                content = f.read()
            status = STATUS_OK

        except (FileNotFoundError, IsADirectoryError) as e:
            logging.info(f"file detecting error. path:{path}, error:{e}")
            path = DOCUMENT_ROOT + NOT_FOUND_DOCUMENT
            with open(path, "br") as f:
                content = f.read()
            status = STATUS_NOT_FOUND

        status_message = HTTP_STATUS_MESSAGE[status]
        ext = os.path.splitext(path)[1][1:]
        mime_type = self.get_mime_type(ext)

        headers = [
            ("Date", datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            ("Server", "Henacorn v0.1"),
            ("Connection", "Close"),
            ("Content-Type", mime_type),
        ]
        start_response(status_message, headers)

        return [content]

    @staticmethod
    def get_mime_type(ext: str) -> str:
        return {
            "txt": "text/plain",
            "html": "text/html",
            "css": "text/css",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
        }.get(ext.lower(), "application/octet-stream")
