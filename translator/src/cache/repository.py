from abc import ABC, abstractmethod


class ICacheRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set_(self, key, value, exp_time_seconds):
        pass
