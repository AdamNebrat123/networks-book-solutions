from scapy.all import *

def get_letter_by_port(packet):
    if UDP in packet:  # אם הפקטה היא של UDP
        if packet.haslayer(Raw) and packet[Raw].load == b'NONE':  # אם יש שכבת Raw ריקה
            letter = chr(packet[UDP].dport)  # המרת הפורט לתו ASCII
            print(f"Received letter: {letter}")  # הדפסת האות

def main():
    print('Sniffing for UDP packets...')
    sniff(filter="udp", prn=get_letter_by_port)  # סינון לפי UDP

if __name__ == '__main__':
    main()