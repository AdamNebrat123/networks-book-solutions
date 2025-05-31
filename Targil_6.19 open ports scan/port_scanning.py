from scapy.all import *
import random
start_port = 20
end_port = 1024
IP_ADDR = input("type an IP address: \n") # 192.168.1.239

for port in range(start_port, end_port + 1):
    syn_segment = TCP(dport=port, seq=random.randint(0, 1000000), flags='S')
    syn_packet = IP(dst=IP_ADDR)/syn_segment
    syn_ack_packet = sr1(syn_packet, timeout = 0.05, verbose=0)
    if syn_ack_packet is None:
        continue
    if syn_ack_packet.haslayer(TCP):
        if syn_ack_packet[TCP].flags == 'SA':
            print("the port {0} is open!".format(port))

print("done")

