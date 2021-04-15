import http.server
import functools
import threading
from typing import Optional

class HttpServer(threading.Thread):
    def __init__(self, httpDir: str, port: Optional[int] = 8080):
        super().__init__(daemon=True, name="HTTP")
        self.httpServer = None
        self._port = port
        self._httpDir = httpDir
        self.start()

    def run(self):
        super().run()
        self.httpServer = http.server.HTTPServer(('', self._port), functools.partial(SimplerHandler, directory=self._httpDir))
        self.httpServer.serve_forever()


class SimplerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extensions_map.update({
            '.js': 'application/javascript'
        })

    def log_message(self, *args):
        pass

    def log_request(self, code='-', size='-'):
        pass