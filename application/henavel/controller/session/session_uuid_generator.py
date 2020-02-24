import uuid
from abc import abstractmethod, ABC


class SessionUUIDGeneratorInterface(ABC):
    @staticmethod
    @abstractmethod
    def generate() -> str:
        pass


class SessionUUIDGenerator:
    """
    SessionUUIDGeneratorのファクトリ
    """

    def __new__(cls, name=None):
        # ビルトインのuuidを使ったやつしかまだない
        if name is None:
            return BuiltInUUIDGenerator()

        raise ValueError(f"SessionIDGenerator of '{name}' is not found.")


class BuiltInUUIDGenerator(SessionUUIDGeneratorInterface):
    @staticmethod
    def generate() -> str:
        return uuid.uuid4().hex
