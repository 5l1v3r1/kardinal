"""
Name: Kardinal
Author: Eternali
Date Created: Dec 2. 2017
Date Modified: Dec 2, 2017
"""

from queue import Queue
from server import Server
from server import nodes

# -------------------------------- Global

LOCALADDR = ("localhost", 10000)

# -------------------------------- Main


def main():

    server_queue = Queue()
    server = Server(server_queue, LOCALADDR)
    server.start()
    print("[**] Listening on {}:{}".format(LOCALADDR[0], LOCALADDR[1]))

    try:
        while True:
            command = input(">> ")
            if command[0] == "/":
                if command.upper() == "/LIST":
                    for node in nodes:
                        print(node.addr)
            else:
                with server.commands.mutex:
                    server.commands.queue.clear()
                server.commands.put(command)
    except KeyboardInterrupt:
        server.shutdown_flag.set()


if __name__ == "__main__":
    main()
