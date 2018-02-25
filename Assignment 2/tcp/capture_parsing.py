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
            connection.start_time = min(connection.start_time, ts)
            connection.end_time = max(connection.end_time, ts)
            if source_ip_address == connection.source_ip_address:
                connection.packets_source_to_destination += 1
                connection.bytes_source_to_destination += len(tcp.data)
            else:
                connection.packets_destination_to_source += 1
                connection.bytes_destination_to_source += len(tcp.data)
            connections[connection] = connection
        return list(connections)


def flag_set(tcp: dpkt.tcp.TCP, flag: int) -> bool:
    """
    Returns whether a flag is set for a TCP packet
    """
    return (tcp.flags & flag) != 0
