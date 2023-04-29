#!/usr/bin/env python3
import sys
import time
import sqlite3
import json
from scapy.all import sniff, get_if_list
from scapy.all import Packet, IPOption, bind_layers
from scapy.all import PacketListField, ShortField, IntField, FieldLenField, BitField
from scapy.all import IP
from scapy.layers.inet import _IPOption_HDR

# create db
conn = sqlite3.connect('monitor.db')
cursor = conn.cursor()
# create table
# Summary, Switches, Start_time, End_time, Packet_size
sql_create = '''CREATE TABLE IF NOT EXISTS ping_data
           (ID INTEGER primary key AUTOINCREMENT,
            Summary TEXT,
            Switches TEXT,
            Start_time INTEGER,
            End_time REAL,
            Packet_size INTEGER);'''
cursor.execute(sql_create)


def get_if(host_iface):
    # ifs=get_if_list()
    iface=None
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


def sendData(pkt):
    if pkt[IP].options[0].size == 0:
         return
    End_time = time.time()
    Summary = pkt[IP].src + ' -> ' + pkt[IP].dst
    option = pkt[IP].options[0]
    Switches = []
    for i in range(0, option.count):
         Switches.append({
              'name': option.swtraces[i].swid,
            #   'time': option.swtraces[i].timestamp,
            #   'end_time': option.swtraces[i].intimestamp,
              'size': option.swtraces[i].size
         })
    Switches.reverse()
    Start_time = option.init_time
    Packet_size = option.size
    Switches = json.dumps(Switches)
    data = [(Summary, Switches, Start_time, End_time, Packet_size)]
    
    cursor.executemany('''INSERT INTO ping_data (Summary, Switches, Start_time, End_time, Packet_size) VALUES (?,?,?,?,?)''', data)
    conn.commit()

def handle_pkt(pkt):
    pkt.show2()
    sendData(pkt)


def main():
    if len(sys.argv)<2:
        print('pass these arguments: <interface>')
        exit(1)
    iface = get_if(sys.argv[1])
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(filter="udp and port 4321", iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()


