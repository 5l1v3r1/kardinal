class Node:

    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        pass

    def send_command(self, command):
        self.sock.send(command.encode("utf-8"))
        return

    def upgrade(self):
        self.sock.send("UPGRADE".encode("utf-8"))
