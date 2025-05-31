import socket


def main():
    try:
        my_socket = socket.socket()
        my_socket.connect(("127.0.0.1", 8200))
        while True:
            msg = input('Input a Command (TIME, WHORU, RAND, EXIT):')
            zfill_length = str(len(msg)).zfill(2)
            msg = zfill_length + msg
            my_socket.send(msg.encode())
            length = my_socket.recv(2).decode()
            if not length.isdigit():
                reply = 'wrong protocol'
                my_socket.send(reply.encode())
                my_socket.recv(1024)
                continue
            data = my_socket.recv(int(length)).decode()
            print("The server sent: " + data)

    except Exception:
        print("connection was interrupted")
    finally:
        my_socket.close()


main()