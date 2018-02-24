import dpkt
from lib.tcp_connection import TCPConnection
import pcapy
from typing import BinaryIO, List

def read_cap_file(filename: str) -> List[TCPConnection]:
    '''
    Returns connections parsed from a TCP trace file
    '''
    f: BinaryIO = open(filename, "rb")
    pcap: dpkt.pcap.Reader = dpkt.pcap.Reader(f)

    connections: List[TCPConnection] = []
    for ts, buf in pcap:
        eth: dpkt.ethernet.Ethernet = dpkt.ethernet.Ethernet(buf)
        ip: dpkt.ip.IP = eth.data
        tcp: dpkt.tcp.TCP = ip.data

        if tcp.dport == 80 and len(tcp.data) > 0:
            http: dpkt.http.Request = dpkt.http.Request(tcp.data)
            # print(http.uri)

    return connections
