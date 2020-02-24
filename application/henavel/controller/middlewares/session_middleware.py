from application.henavel.controller.http.cookie import Cookie
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response
from application.henavel.controller.routing.middleware.middleware import Middleware
from application.henavel.controller.session.session_manager import SessionManager


class SessionMiddleware(Middleware):
    SESSION_MANAGER = SessionManager()
    SESSION_ID_NAME = "HENASESSION_ID"
    SESSION_LIFETIME = 10

    def __init__(self):
        self.next_cookie = None
        self.session = None

    def before(self, request: Request) -> Request:
        manager = self.__class__.SESSION_MANAGER
        session = None

        session_cookie = request.cookies.get(self.__class__.SESSION_ID_NAME)
        if session_cookie is not None:
            uuid = session_cookie.value
            session = manager.get_session(uuid)

        if session is None:
            session = manager.create_session()

        request.session = session
        self.session = session
        return request

    def after(self, response: Response) -> Response:
        session_cookie = Cookie(
            name=self.__class__.SESSION_ID_NAME,
            value=self.session.uuid,
            max_age=self.__class__.SESSION_LIFETIME,
        )
        response.cookies.save(session_cookie)
        return response
