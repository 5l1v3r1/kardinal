from queue import Queue
from server import Server

#### GLOBAL CONSTANTS ####

LOCALADDR = ("localhost", 10000)

#### MAIN FUNCTION ####

def main ():

    server_queue = Queue()
    server = Server(server_queue, LOCALADDR)
    server.start()
    print("[**] Listening on {}:{}".format(LOCALADDR[0], LOCALADDR[1]))

    try:
        while True:
            command = input(">> ")
            server.commands.put(command)
    except KeyboardInterrupt:
        server.shutdown_flag.set()


if __name__ == "__main__":
    main()
