#!/usr/bin/env python3
import sys
import socket
import time
from scapy.all import sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import Ether, IP, UDP, bind_layers
from scapy.all import IntField, FieldLenField, ShortField, PacketListField, BitField
from scapy.layers.inet import _IPOption_HDR
from time import sleep


# tmux a -t show

def get_if(host_iface):
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if host_iface in i:
            iface=i
            break;
    if not iface:
        print("Cannot find " + host_iface + " interface")
        exit(1)
    return iface

class SwitchTrace(Packet):
    fields_desc = [ IntField("swid", 0),
                    IntField("size", 0)]
    def extract_padding(self, p):
                return "", p

class IPOption_MONITOR(IPOption):
    name = "MONITOR"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="swtraces",
                                  adjust=lambda pkt,l:l*2+12),
                    ShortField("count", 0),
                    IntField("size", 0),
                    BitField("init_time", 0, 48),
                    PacketListField("swtraces", [], SwitchTrace, count_from=lambda pkt:(pkt.count*1)) ]


def main():
    if len(sys.argv)<5:
        print('pass these arguments: <interface> <destination> "<message>" <duration>')
        exit(1)

    iface = get_if(sys.argv[1])
    addr = socket.gethostbyname(sys.argv[2])

    # pkt = Ether(src=get_if_hwaddr(iface), dst="ff:ff:ff:ff:ff:ff") / IP(
    #    dst=addr, options = IPOption_MONITOR(count=2,
    #        swtraces=[SwitchTrace(swid=0, timestampin=0, timestampout=0), SwitchTrace(swid=1, timestampin=0, timestampout=0)])) / UDP(
    #        dport=4321, sport=1234) / sys.argv[2]
    
    
    # hexdump(pkt)
    try:
      for i in range(int(sys.argv[4])):
        pkt = Ether(src=get_if_hwaddr(iface), dst="ff:ff:ff:ff:ff:ff") / IP(
        dst=addr, options = IPOption_MONITOR(count=0, init_time=int(time.time()), swtraces=[])) / UDP(
            dport=4321, sport=1234) / sys.argv[3]
        
        pkt.show2()

        sendp(pkt, iface=iface)
        sleep(1)
    except KeyboardInterrupt:
        raise

if __name__ == '__main__':
    main()