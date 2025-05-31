from scapy.all import *


def filter(packet):
    return packet.haslayer(IP) and (packet[IP].src == '142.250.75.132' or packet[IP].dst == '142.250.75.132')

def print_summary(packet):
    print(packet.summary())

def main():

    print('sniffing')
    packets = sniff(count = 1, lfilter = filter, prn = print_summary)

if __name__ == '__main__':
    main()