
import socketserver

from src.cache.redis import get_cache_repository
from src.config.env import (CACHE_ENABLED, DEFAULT_LANGUAGE_SRC,
                            LANGUAGE_AUTODETECT_ENABLED, LANGUAGE_TARGET,
                            MAX_PAYLOAD_SIZE, SERVER_PORT)
from src.identifier.identifier import get_identifier_repository
from src.translator.dl_translate import get_translate_repository

translator = get_translate_repository()
cache = get_cache_repository()
identifier = get_identifier_repository()

class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(MAX_PAYLOAD_SIZE)
        data = data.decode('utf-8')

        if CACHE_ENABLED:
            cached = cache.get(data)
            if cached:
                self.request.send(cached.encode('utf-8') + b'\n')
                return
        if LANGUAGE_AUTODETECT_ENABLED:
            lang_source = identifier.identify(str(data))
        else:
            lang_source = DEFAULT_LANGUAGE_SRC

        translated_data = \
            translator.parse(text=data, lang_src=lang_source, lang_dest=LANGUAGE_TARGET)

        if CACHE_ENABLED:
            cache.set_(data, translated_data, 3600)

        self.request.send(translated_data.encode('utf-8') + b'\n')


class TranslateServer():
    def __init__(self, port=SERVER_PORT):
        self.server = socketserver.ThreadingTCPServer(('0.0.0.0', port), Handler)

    def serve(self):
        self.server.serve_forever()
