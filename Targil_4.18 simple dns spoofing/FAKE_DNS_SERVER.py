import socket

DNS_SERVER_IP = '0.0.0.0'
DNS_SERVER_PORT = 53
DEFAULT_BUFFER_SIZE = 1024

def dns_handler(data, client_address):
    """
    Handles DNS query from client.
    If domain == 'www.google.co.il', sends back a spoofed response with IP 212.143.70.40
    """
    # בדיקה שהבקשה היא A query עבור il.co.google.www

    print(f"Raw data: {data.hex()}")

    if b'\x06google\x02co\x02il\x00' in data and data[2] == 1:
        print("Got DNS query for www.google.co.il from", client_address)

        # קודם כל העתקה של ההתחלה של הבקשה אחד לאחד ואז הוספת דברים של תגובה
        transaction_id = data[:2] # אלה שני הבתים הראשונים
        flags = b'\x81\x80'
        qdcount = b'\x00\x01'
        ancount = b'\x00\x01'
        nscount = b'\x00\x00'
        arcount = b'\x00\x00'

        header = transaction_id + flags + qdcount + ancount + nscount + arcount

        question = data[12:]  # השאלה המקורית (הכתובת) (ההתחלה של המידע מתחילה בהדר ולכן אני חותך ב12)

        answer_name = b'\xc0\x0c'    # הצבעה על שם הדומיין בשאלה
        answer_type = b'\x00\x01'  # A record
        answer_class = b'\x00\x01'
        ttl = b'\x00\x00\x00\x3c'  # 60 שניות
        rdlength = b'\x00\x04'
        rdata = socket.inet_aton("212.143.70.40")  # IP שאנחנו רוצים להחזיר

        answer = answer_name + answer_type + answer_class + ttl + rdlength + rdata

        response = header + question + answer

        server_socket.sendto(response, client_address)
    else:
        print("Got unhandled DNS query from", client_address)

def dns_udp_server(ip, port):
    """
    Starts a UDP server on a given IP:PORT, and calls
    dns_handler(data, client_address) on any client request data.
    """
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print("Server started successfully! Waiting for data..")
    while True:
        try:
            data, addr = server_socket.recvfrom(DEFAULT_BUFFER_SIZE)
            dns_handler(data, addr)
        except Exception as ex:
            print("Client exception! %s" % (str(ex), ))

def main():
    """
    Main execution point of the program
    """
    print("Starting UDP server..")
    dns_udp_server(DNS_SERVER_IP, DNS_SERVER_PORT)

if __name__ == '__main__':
    main()
