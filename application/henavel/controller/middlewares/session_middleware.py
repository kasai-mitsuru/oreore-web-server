import uuid
from abc import ABC, abstractmethod
from typing import Dict


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
