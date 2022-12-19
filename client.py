import socket
import threading

FORMAT = 'utf-8'
HEADER = 64
PORT = 5050
SERVER = "# IPv4 address here"
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # to connect with ip address family
client.connect(ADDR)


def handle_inp():
    print(client.recv(2048).decode(FORMAT))


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)


print("Press 0 Disconnect")
while True:
    thread = threading.Thread(target=handle_inp)  # To use call handle input in other thread
    thread.start()
    m = input("Enter message::")
    if m == "0":
        send(DISCONNECT_MSG)
        break
    send(m)
    thread = threading.Thread(target=handle_inp)  # To use call handle input in other thread
    thread.start()
