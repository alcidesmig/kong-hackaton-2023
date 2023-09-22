from abc import ABC, abstractmethod


class ITranslateRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, text: str, lang_src: str, lang_dest: str):
        pass
