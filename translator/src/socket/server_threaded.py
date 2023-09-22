import os
import socketserver

from src.cache.redis import get_cache_repository
from src.translator.dl_translate import get_translate_repository

LANG_SOURCE = "Portuguese"
LANG_DEST = "English"

translator = get_translate_repository()
cache = get_cache_repository()

class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(4096)
        data = data.decode('utf-8')

        if os.getenv("CACHE"):
            cached = cache.get(data)
            if cached:
                self.request.send(cached.encode('utf-8') + b'\n')
                return
        translated_data = \
            translator.parse(text=data, lang_src=LANG_SOURCE, lang_dest=LANG_DEST)

        if os.getenv("CACHE"):
            cache.set_(data, translated_data, 3600)

        self.request.send(translated_data.encode('utf-8') + b'\n')


class TranslateServer():
    def __init__(self, port=25564):
        self.server = socketserver.ThreadingTCPServer(('0.0.0.0', port), Handler)

    def serve(self):
        self.server.serve_forever()
