import dpkt
import socket
from tcp.connection import TCPConnection
from typing import BinaryIO, Dict, List, Set

def read_cap_file(filename: str) -> List[TCPConnection]:
    """
    Returns connections parsed from a TCP trace file
    """
    with open(filename, "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        # Hack using keys and values both as TCPConnection
        # so I can keep a unique set of TCPConnections and with O(1) lookup
        connections: Dict[TCPConnection, TCPConnection] = {}
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            source_ip_address = socket.inet_ntoa(ip.src)
            destination_ip_address = socket.inet_ntoa(ip.dst)
            source_port = tcp.sport
            destination_port = tcp.dport
            connection = TCPConnection(source_ip_address,
                                       destination_ip_address,
                                       source_port,
                                       destination_port)
            if connection in connections:
                connection = connections[connection]
            if flag_set(tcp, dpkt.tcp.TH_SYN):
                connection.syn_count += 1
            if flag_set(tcp, dpkt.tcp.TH_ACK):
                connection.ack_count += 1
            if flag_set(tcp, dpkt.tcp.TH_FIN):
                connection.fin_count += 1
            if flag_set(tcp, dpkt.tcp.TH_RST):
                connection.rst_count += 1
            if ts < connection.start_time:
                connection.start_time = ts
            if ts > connection.end_time:
                connection.end_time = ts
            connections[connection] = connection
        return list(connections)


def flag_set(tcp: dpkt.tcp.TCP, flag: int) -> bool:
    """
    Returns whether a flag is set for a TCP packet
    """
    return (tcp.flags & flag) != 0
