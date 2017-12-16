"""
Name: Kardinal
Author: Eternali
Date Created: Dec 2. 2017
Date Modified: Dec 2, 2017
"""

import math
from queue import Queue
from command import Command
from server import nodes
from server import Server

# -------------------------------- Global

LOCALADDR = ("localhost", 10000)
TABSIZE = 4

# define valid utility commands

def to_table(headers, contents, horiz_divide="\t\t"):
    table = ""
    table += "".join([header + horiz_divide for header in headers]) + "\n"
    table += "\n".join([horiz_divide.join(str(col) for col in row) for row in contents])
    return table


def calc_tab(cur_len, max_len):
    return (max_len - cur_len + 4) * " "


# -------------------------------- Main


def main():

    server_queue = Queue()
    server = Server(server_queue, LOCALADDR)
    server.setDaemon(True)


    # command functions (those that are too complex for lambdas)
    def shutdown ():
        print("\n[**] Shutting down Kardinal.\n")
        server.shutdown_flag.set()
        exit(0)

    def set_targets ():
        print("\nAvailable nodes:")
        print("\n{}\n".format(to_table(("INDEX", "IP ADDRESS", "PORT"),
                 [(n + 1, node.addr[0], node.addr[1]) for n, node in enumerate(nodes)])))
        print("Current targets:")
        print("\n{}\n".format(to_table(("INDEX", "IP ADDRESS", "PORT"),
                 [(n + 1, node.addr[0], node.addr[1]) for n, node in enumerate(nodes) if node.is_target])))
        targets = [int(t) - 1 for t in input("Enter space separated list of indices: ").split(" ")]
        for n, node in enumerate(nodes):
            node.is_target = True if n in targets else False

    # command list
    commands = [
        Command("LIST", "Show all connected nodes.",
                (lambda: "\n{}\n".format(to_table(("IP ADDRESS", "PORT"), [node.addr for node in nodes])))),
        Command("CLEAR", "Clear the screen.", (lambda: chr(27) + "[2J")),
        Command("EXIT", "Shutdown Kardinal.", shutdown),
        Command("SET_TARGETS", "Set targets for next set of commands", set_targets),
        Command("LIST_TARGETS", "List all currently selected targets",
                (lambda: "\n{}\n".format(to_table(("IP ADDRESS", "PORT"), [node.addr for node in nodes if node.is_target]))))
    ]
    # NOTE: must put help outside list literal to avoid "commands uninitialized" error
    commands.append(Command("HELP", "Show this help.",
                            (lambda: "\n" + "\n".join(["/" + cmd.name
                            + calc_tab(len(cmd.name), max([len(c.name) for c in commands]))
                            + cmd.desc for cmd in commands]) + "\n")))


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
