import socket
import threading
from datetime import datetime

clients = []
usernames = []

FORMAT = 'utf-8'
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # IPv4 address here
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # to connect with ip address family
server.bind(ADDR)  # bound socket with address


def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))


# To handle communication in parallel for each
def handle_client(conn, addr):
    # message format ::: "5"
    #                    "Hello"
    print(f"{addr} Connected")
    connected = True
    while connected:
        index = clients.index(conn)
        msg = conn.recv(2048).decode(FORMAT)  # To get actual message
        if msg == DISCONNECT_MSG:
            uname = usernames[index]
            usernames.remove(uname)
            conn.send(f"Form server::DISCONNECTED".encode(FORMAT))
            conn.close()
            clients.remove(conn)
            broadcast(f"{uname} Left the server")
            connected = False
            break
        # print(f"{addr} :: {msg}")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        broadcast(f"{usernames[index]}:: {msg}  {current_time}\n")

    # To handle connection


def start():
    server.listen()  # to listen to connections
    print(f"Listening on {SERVER}, Port {PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        conn.send("UNAME:".encode(FORMAT))
        u = conn.recv(1024).decode(FORMAT)
        usernames.append(u)
        broadcast(f"--{u} Joined--")
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # To use call handle client in other thread
        thread.start()
        print(f"Active connections::: {threading.activeCount() -1}")


print("Server is starting")
start()