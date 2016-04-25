from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import Queue, time

class MyServerProtocol(WebSocketServerProtocol):
    __q = None
    def onConnect(self, request):
        pass

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        MyServerProtocol.__q.put(payload)

    def onClose(self, wasClean, code, reason):
        pass

    @staticmethod
    def setQueue(q):
        MyServerProtocol.__q = q
        print q
