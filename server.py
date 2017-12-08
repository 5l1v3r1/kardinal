"""
Classes for server listening threads

Author: Eternali
Date Created: Dec 2, 2017
Date Modified: Dec 2, 2017
"""

import threading
import socket
import sys
from queue import Queue

from node import Node

nodes = []

class NodeListener(threading.Thread):

    def __init__(self, server):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.server = server
        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            client, addr = self.server.accept()
            nodes.append(Node(Queue(), client, addr))
            sys.stdout.write("Connected to: {}:{}\n>> ".format(addr[0], addr[1]))
            sys.stdout.flush()

        sys.stdout.write("[**] Shutting down node thread.")
        sys.stdout.flush()
        return


class Server(threading.Thread):

    def __init__(self, commands, localaddr):
        threading.Thread.__init__(self, args=(), kwargs=None)

        self.localaddr = localaddr
        self.commands = commands
        self.shutdown_flag = threading.Event()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.localaddr)
        self.server.listen(10)

    def run(self):
        # start node listener thread
        node_listener = NodeListener(self.server)
        node_listener.start()
        while not self.shutdown_flag.is_set():
            cmd = self.commands.get()
            if cmd is None:
                break
            self.run_command(cmd)

        sys.stdout.write("[**] Shutting down server.")
        sys.stdout.flush()
        node_listener.shutdown_flag.set()
        for node in nodes:
            node.shutdown()
        self.server.close()
        return

    def run_command(self, cmd):
        for node in nodes:
            if node.is_target:
                # with node.queue.mutex:
                #     node.queue.queue.clear()
                node.queue.put(cmd)
