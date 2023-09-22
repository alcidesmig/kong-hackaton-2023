import socketserver
import time
import dl_translate as dlt

LANG_SOURCE = "Portuguese"
LANG_DEST = "English"

global mt
mt = dlt.TranslationModel()
print(mt)
class TranslationHandler(socketserver.BaseRequestHandler):
    def _translate(self, message):
        return
    def handle(self):
        data = self.request.recv(1024)
        response = data.decode('utf-8')
        print(response)
        response = mt.translate(response, source=LANG_SOURCE, target=LANG_DEST)
        print(response, mt)
        self.request.send(response.encode('utf-8') + b'\n')

server = socketserver.ThreadingTCPServer(('0.0.0.0', 25564), TranslationHandler)
server.serve_forever()

