from abc import abstractmethod, ABC
from typing import Dict

from application.henavel.controller.session.session import Session
from application.henavel.controller.session.session_uuid_generator import (
    SessionUUIDGenerator,
)


class SessionManagerInterface(ABC):
    @abstractmethod
    def get_session(self, uuid: str, access: bool) -> Session:
        pass

    @abstractmethod
    def create_session(self) -> Session:
        pass

    @abstractmethod
    def remove_session(self, uuid: str) -> "SessionManagerInterface":
        pass


class SessionManager:
    # セッションマネージャーのファクトリー
    def __new__(cls, name=None):
        # まだインメモリセッションマネージャーしか実装していない
        if not name:
            return InMemorySessionManager()

        raise ValueError(f"SessionManager of '{name}' is not found.")


class InMemorySessionManager(SessionManagerInterface):
    def __init__(self):
        super().__init__()
        self.sessions: Dict[str, Session] = {}

    def get_session(self, uuid: str, access: bool = True) -> Session:
        session = self.sessions.get(uuid)

        if session and access:
            session.access()

        return session

    def create_session(self) -> Session:
        uuid = SessionUUIDGenerator().generate()
        session = Session(uuid=uuid)
        self.sessions[session.uuid] = session
        return session

    def remove_session(self, uuid: str) -> "InMemorySessionManager":
        if uuid in self.sessions:
            del self.sessions[uuid]
        return self
