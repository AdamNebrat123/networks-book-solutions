import socket
from datetime import datetime
import random

def main():
    try:

        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 8200))
        server_socket.listen()
        print("Server is up and running")
        (client_socket, client_address) = server_socket.accept()
        print("Client connected")
        while True:
            length = client_socket.recv(2).decode()
            if not length.isdigit():
                reply = 'wrong protocol'
                client_socket.send(reply.encode())
                client_socket.recv(1024)
                continue
            data = client_socket.recv(int(length)).decode()
            print("Client sent: " + data)
            if data == 'TIME':
                reply = datetime.now()
            elif data == 'WHORU':
                reply = 'Adam\'s server'
            elif data == 'RAND':
                reply = random.randint(1, 10)
            elif data == 'EXIT':
                reply = 'exiting now'
                break
            else:
                reply = 'unknown command: ' + data

            reply = str(reply)
            zfill_length = str(len(reply)).zfill(2)
            reply = zfill_length + reply
            client_socket.send(reply.encode())

    except Exception:
        print("connection was interrupted")

    finally:
        client_socket.close()
        server_socket.close()


main()