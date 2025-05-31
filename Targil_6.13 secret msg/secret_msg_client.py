from scapy.all import *

def send_letter_to_correct_port(letter):
    dport = ord(letter)
    packet = IP(dst='192.168.1.29') / UDP(dport=dport) / Raw('NONE')
    packet.show()
    send(packet)
    print('sent to port {0}'.format(dport))



def main():
    secret_msg = input('hello client, what do you want to send to the server? \n')
    for letter in secret_msg:
        send_letter_to_correct_port(letter)
    print('successfully send the msg!')
if __name__ == '__main__':
    main()