
import socketserver

from src.cache.redis import get_cache_repository
from src.config.env import (
    CACHE_ENABLED,
    DEFAULT_LANGUAGE_SRC,
    LANGUAGE_AUTODETECT_ENABLED,
    LANGUAGE_TARGET,
    MAX_PAYLOAD_SIZE,
    SERVER_PORT,
)
from src.identifier.identifier import get_identifier_repository
from src.translator.dl_translate import get_translate_repository

translator = get_translate_repository()
cache = get_cache_repository()
identifier = get_identifier_repository()

class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(MAX_PAYLOAD_SIZE)
        data = data.decode('utf-8')


        # X-Translate-To:Portuguese;<texto>
        # <texto>

        if data.startswith("X-Translate-To"):
            data_parsed = data.split(";")
            language_metadata = data_parsed[0]
            target_language = language_metadata.split(":")[1]
            target_text = data_parsed[1]
        else:
            target_text = data
            target_language = LANGUAGE_TARGET

        if CACHE_ENABLED:
            cached = cache.get(data)
            if cached:
                self.request.send(cached.encode('utf-8') + b'\n')
                return
        if LANGUAGE_AUTODETECT_ENABLED:
            lang_source = identifier.identify(str(target_text))
        else:
            lang_source = DEFAULT_LANGUAGE_SRC

        translated_data = \
            translator.parse(text=target_text, lang_src=lang_source, lang_dest=target_language)

        if CACHE_ENABLED:
            cache.set_(data, translated_data, 3600)

        self.request.send(translated_data.encode('utf-8') + b'\n')


class TranslateServer():
    def __init__(self, port=SERVER_PORT):
        self.server = socketserver.ThreadingTCPServer(('0.0.0.0', port), Handler)

    def serve(self):
        self.server.serve_forever()
