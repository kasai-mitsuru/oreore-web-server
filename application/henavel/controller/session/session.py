from datetime import datetime
from typing import Dict


class Session:
    def __init__(
        self,
        uuid: str,
        attr: Dict = None,
        first_accessed: datetime = None,
        last_accessed: datetime = None,
    ):
        if attr is None:
            attr = {}
        if first_accessed is None:
            first_accessed = datetime.now()
        if last_accessed is None:
            last_accessed = datetime.now()

        self.uuid: str = uuid
        self.attributes: Dict = attr
        self.first_accessed: datetime = first_accessed
        self.last_accessed: datetime = last_accessed

    def __getitem__(self, item):
        if item in self.attributes:
            return self.attributes[item]

        raise KeyError(f"session does not have '{item}'.")

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def get(self, key, default=None):
        return self.attributes.get(key, default)

    def access(self) -> "Session":
        self.last_accessed = datetime.now()
        return self
