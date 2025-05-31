import socket
import time
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
start = time.perf_counter()
my_socket.sendto('Omer'.encode(), ('127.0.0.1', 8821))
(data, remote_address) = my_socket.recvfrom(1024)
end = time.perf_counter()
print(end)
print('The server sent: ' + data.decode())
my_socket.close()
