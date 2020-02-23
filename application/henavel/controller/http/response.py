from typing import Union

from application.henavel.controller.http import consts
from application.settings import NOT_FOUND_FILE


class Response:
    status_code = consts.STATUS_OK

    def __init__(
        self,
        status_code: int = 0,
        reason_phrase: str = "",
        content_type: str = "",
        content: Union[bytes, str] = "",
    ):
        self.status_code: int = status_code if status_code else self.__class__.status_code
        self.reason_phrase: str = reason_phrase
        self.content_type: str = content_type
        self.content: Union[bytes, str] = content


class ResponseRedirect(Response):
    status_code = consts.STATUS_REDIRECT

    def __init__(self, location: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location


class ResponseBadRequest(Response):
    status_code = consts.STATUS_BAD_REQUEST


class ResponseNotFound(Response):
    status_code = consts.STATUS_NOT_FOUND

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.content:
            with open(NOT_FOUND_FILE) as f:
                self.content = f.read()


class ResponseServerError(Response):
    status_code = consts.STATUS_SERVER_ERROR
