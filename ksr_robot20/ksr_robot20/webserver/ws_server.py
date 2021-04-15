from typing import Union, Callable, Optional
import websockets
import asyncio
import threading
import enum
import copy
import json

class WsServer(threading.Thread):
    def __init__(self, recvCallback, port=4342):
        super().__init__(daemon=True, name="WsServer")
        self._port = port
        self._eventLoop = None
        self._clients = []
        self._clientLock = threading.Lock()
        self.recvCallback = recvCallback
        self.start()
    
    def send(self, data):
        data = json.dumps(data)
        with self._clientLock:
            for client in self._clients:
                try:
                    asyncio.run_coroutine_threadsafe(client.send(data), loop=self._eventLoop)
                except websockets.ConnectionClosed:
                    pass

    def run(self):
        self._eventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._eventLoop)
        self._server = self._eventLoop.run_until_complete(websockets.server.serve(self._recNewConn, host='', port=self._port))
        try:
            self._eventLoop.run_forever()
        finally:
            self._eventLoop.close()

    async def _recNewConn(self, conn, url):
        with self._clientLock:
            self._clients.append(conn)
        while not conn.closed:
            try:
                data = await conn.recv()
            except websockets.ConnectionClosed:
                break
            self.recvCallback(json.loads(data))
        with self._clientLock:
            self._clients.remove(conn)
