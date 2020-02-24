import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict

from application.henavel.controller.http.cookie import Cookie
from application.henavel.controller.http.request import Request
from application.henavel.controller.http.response import Response
from application.henavel.controller.routing.middleware.middleware import Middleware


class IDGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate() -> str:
        pass


class HexUUIDGenerator(IDGenerator):
    @staticmethod
    def generate() -> str:
        return uuid.uuid4().hex


class SessionIDGenerator:
    generators: Dict[str, IDGenerator] = {"hex_uuid": HexUUIDGenerator}

    def __init__(self, name=None):
        self.generator: IDGenerator
        if name is None:
            generator = HexUUIDGenerator
        elif name in self.generators:
            generator = self.generators[name]
        else:
            raise ValueError(f"SessionIDGenerator of '{name}' is not found.")

        self.generator = generator

    def generate(self) -> str:
        return self.generator.generate()


class Session:
    def __init__(
        self,
        id: str = None,
        attr: Dict = None,
        first_accessed: datetime = None,
        last_accessed: datetime = None,
    ):
        if id is None:
            id = SessionIDGenerator().generate()
        if attr is None:
            attr = {}
        if first_accessed is None:
            first_accessed = datetime.now()
        if last_accessed is None:
            last_accessed = datetime.now()

        self.id = id
        self.attributes = attr
        self.first_accessed = first_accessed
        self.last_accessed = last_accessed

    def __getitem__(self, item):
        if item in self.attributes:
            return self.attributes[item]

        raise KeyError(f"session does not have '{item}'.")

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def access(self) -> "Session":
        self.last_accessed = datetime.now()
        return self


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        logging.debug("Session Manager is created.")

    def get_session(self, id: str, access: bool = True) -> Session:
        session = self.sessions.get(id)

        if session and access:
            session.access()

        return session

    def create_session(self) -> Session:
        session = Session()
        self.sessions[session.id] = session
        return session

    def remove_session(self, id: str) -> "SessionManager":
        if id in self.sessions:
            del self.sessions[id]
        return self


class SessionMiddleware(Middleware):
    SESSION_MANAGER = SessionManager()
    SESSION_ID_NAME = "HENASESSION_ID"
    SESSION_LIFETIME = 5

    def __init__(self):
        self.next_cookie = None
        self.session = None

    def before(self, request: Request) -> Request:
        manager = self.__class__.SESSION_MANAGER
        session = None

        session_cookie = request.cookies.get(self.__class__.SESSION_ID_NAME)
        if session_cookie is not None:
            session_id = session_cookie.value
            session = manager.get_session(session_id)

        if session is None:
            session = manager.create_session()

        request.session = session
        self.session = session
        return request

    def after(self, response: Response) -> Response:
        session_cookie = Cookie(
            name=self.__class__.SESSION_ID_NAME,
            value=self.session.id,
            max_age=self.__class__.SESSION_LIFETIME,
        )
        response.cookies.save(session_cookie)
        return response
