from scapy.all import *





def main():

    domain = input('enter a domain that you want his ip: \n')
    dns_packet = IP(dst='8.8.8.8') / UDP(sport=8200, dport=53) / DNS(qdcount = 1,qd=DNSQR(qname=domain), rd=1) / DNSQR(qname=domain)
    print(dns_packet.show())
    response_packet = sr1(dns_packet)
    for dns_rr in response_packet[DNS].an:
        if dns_rr.type == 1:  # 1 means type A ( domain ti ip )
            print(dns_rr.rdata)


if __name__ == '__main__':
    main()