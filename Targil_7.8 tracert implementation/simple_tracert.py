from scapy.all import *
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python my_traceroute.py <destination>")
    sys.exit(1)
DST = socket.gethostbyname(sys.argv[1])
MAX_HOPS = 50
for ttl in range(1, MAX_HOPS + 1, 1):
    tracert_packet = IP(dst=DST, ttl=ttl)/ICMP()
    start_time = time.time()
    reply_packet = sr1(tracert_packet,verbose=0, timeout=1)
    end_time = time.time()

    if not reply_packet: #if the packet is None
        print(f"{ttl}: * * * Request timed out.")
    else:

        rtt = (end_time - start_time) * 1000  # מילישניות

        print(f"{ttl}: {reply_packet.src}  {rtt:.2f} ms")

        if reply_packet.src == DST:
            print('Trace complete.')
            break
