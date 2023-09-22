

import dl_translate as dlt
from src.translator.repository import ITranslateRepository

global mt

mt = dlt.TranslationModel()

class TranslateRepository(ITranslateRepository):
    def __init__(self):
        pass

    def parse(self, text: str, lang_src: str, lang_dest: str):
        return mt.translate(text, source=lang_src, target=lang_dest)


def get_translate_repository() -> ITranslateRepository:
    return TranslateRepository()
