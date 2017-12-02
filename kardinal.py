from queue import Queue
from server import Server

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
            with server.commands.mutex:
                server.commands.queue.clear()
            server.commands.put(command)
    except KeyboardInterrupt:
        server.shutdown_flag.set()


if __name__ == "__main__":
    main()
