"""
Classes for node handler threads

Author: Eternali
Date Created: Dec 2, 2017
Date Modified: Dec 2, 2017
"""

import threading


class NodeThread(threading.Thread):

    def __init__(self, queue, sock):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.sock = sock
        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            cmd = self.queue.get()
            # if the command sent is None, end the thread
            if cmd is None:
                break
            self.run_command(cmd)

        self.sock.close()
        return

    def run_command(self, cmd):
        self.sock.send(cmd.encode("utf-8"))
        # print("Sent {} on thread {}.".format(cmd, threading.currentThread().getName()))


class Node:

    def __init__(self, queue, client, addr, is_target=True):
        self.queue = queue
        self.client = client
        self.addr = addr
        self.is_target = is_target

        self.handler = NodeThread(queue, client)
        self.handler.start()

    def shutdown():
        self.handler.shutdown_flag.set()
