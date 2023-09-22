from abc import ABC, abstractmethod


class IIdentifierRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def identify(self, text: str) -> str:
        pass
