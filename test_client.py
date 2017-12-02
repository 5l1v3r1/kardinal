import socket

TARGETADDR = ("127.0.0.1", 12345)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(TARGETADDR)

while True:
    data = client.recv(4096)
    print("\r{}".format(data), end="", flush=True)