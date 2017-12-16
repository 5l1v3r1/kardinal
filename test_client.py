import socket

TARGETADDR = ("localhost", 10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(TARGETADDR)

while True:
    data = client.recv(4096)
    print("\r{}".format(data), end="", flush=True)