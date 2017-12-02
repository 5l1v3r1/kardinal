import threading
import socketserver

class Node(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        ct = threading.currentThread()
        resp = "{}: {}".format(ct.getName(), data)
        self.request.send(resp.encode("utf-8"))
        return
