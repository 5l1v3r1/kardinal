import threading
import socket
import socketserver

from node import Node

#### GLOBAL CONSTANTS ####
LOCALADDR = ("localhost", 12345)


class ThreadedCCServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


#### MAIN FUNCTION ####

def main ():
    server = ThreadedCCServer(LOCALADDR, Node)
    ip, port = server.server_address

    main_thread = threading.Thread(target=server.serve_forever)
    main_thread.setDaemon(True)
    main_thread.start()

    print("Server loop now running")

    # connect to the Server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    # send test data
    msg = "Hello world"
    sent_len = sock.send(msg.encode("utf-8"))
    print("Sent {}".format(msg))

    # receive test data
    resp = sock.recv(1024)
    print("Received {}".format(resp))

    #clean up
    sock.close()
    server.socket.close()


if __name__ == "__main__":
    main
