"""
Name: Kardinal
Author: Eternali
Date Created: Dec 2. 2017
Date Modified: Dec 2, 2017
"""

from queue import Queue
from command import Command
from server import nodes
from server import Server

# -------------------------------- Global

LOCALADDR = ("localhost", 10000)

# define valid utility commands

def to_table(headers, contents, horiz_divide="\t\t"):
    table = ""
    table += "".join([header + horiz_divide for header in headers]) + "\n"
    table += "\n".join([horiz_divide.join(str(col) for col in row) for row in contents])
    return table


# -------------------------------- Main


def main():

    server_queue = Queue()
    server = Server(server_queue, LOCALADDR)
    server.setDaemon(True)


    def shutdown ():
        print("\n[**] Shutting down Kardinal.\n")
        server.shutdown_flag.set()
        exit(0)


    commands = [
        Command("LIST", "Show all connected nodes.",
                (lambda: "\n{}\n".format(to_table(("IP ADDRESS", "PORT"), [node.addr for node in nodes])))),
        Command("EXIT", "Shutdown Kardinal.", shutdown)
    ]
    # NOTE: must put help outside list literal to avoid "commands uninitialized" error
    commands.append(Command("HELP", "Show this help.",
                            (lambda: "\n" + "\n".join(["/" + cmd.name + "\t\t" + cmd.desc for cmd in commands]) + "\n")))


    server.start()
    print("[**] Listening on {}:{}".format(LOCALADDR[0], LOCALADDR[1]))

    try:
        while True:
            requested_cmd = input(">> ")
            if requested_cmd[0] == "/":
                for cmd in commands:
                    if requested_cmd[1:].upper() == cmd.name:
                        print(cmd.todo())
            else:
                with server.commands.mutex:
                    server.commands.queue.clear()
                server.commands.put(requested_cmd)
    except KeyboardInterrupt:
        server.shutdown_flag.set()


if __name__ == "__main__":
    main()
