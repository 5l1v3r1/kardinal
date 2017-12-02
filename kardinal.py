import socket
from node import Node


class sockethadler:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((socket.gethostname(), 10000))
        self.s.listen(30)

    def expect_connections(self):
        (clientsocket, address) = socket.accept()
        return Node(clientsocket, address)


s0 = sockethadler()


while True:
    nodes_list.append(s0.expect_connections())
