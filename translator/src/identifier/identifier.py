from lingua import LanguageDetectorBuilder
from src.identifier.repository import IIdentifierRepository

global lang_detec
lang_detec = LanguageDetectorBuilder.\
    from_all_languages().\
        with_preloaded_language_models().\
            build()

class LinguaRepository(IIdentifierRepository):
    def __init__(self):
        pass

    @staticmethod
    def _format_lang(lang):
        return str(lang)[9:].capitalize()

    def identify(self, text: str) -> str:
        return self._format_lang(lang_detec.detect_language_of(text))

def get_identifier_repository() -> IIdentifierRepository:
    return LinguaRepository()
