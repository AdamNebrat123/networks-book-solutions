from http.client import responses

from scapy.all import *

ADDR = input('enter a IP address that you want to ping: \n')
NUM_OF_PACKETS = input('enter how many ping packets you want to send: \n')
NUM_OF_PACKETS = int(NUM_OF_PACKETS)
print(f'Sending {NUM_OF_PACKETS} packets to {ADDR}')
request_packet = IP(dst=ADDR)/ ICMP(type=8,id= 100)/'abcd'
answered, unanswered = sr( (request_packet * NUM_OF_PACKETS) , timeout = 1, verbose = 0 )
if not unanswered:
    print('every packet got a reply!!')
if answered:
    print(f'got {len(answered)} replies from {ADDR}')
else:
    print(f'got 0 replies from {ADDR}')
