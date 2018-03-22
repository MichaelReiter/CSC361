import dpkt
import socket
from traceroute.ip_protocols import ip_protocol_map
from traceroute.results_logger import print_results
from typing import Dict, List

def read_trace_file(filename: str) -> (str, str, List[str], Dict[int, str]):
    """
    Returns source IP, destination IP, intermediate IPs
    and protocols parsed from a trace file
    """
    with open(filename, "rb") as f:
        pcap = dpkt.pcapng.Reader(f)
        intermediate_ip_addresses = []
        protocols = {}
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            # Filter out non IP packets
            if type(ip) == dpkt.ip.IP:
                if ip.ttl == 1:
                    source_ip_address = socket.inet_ntoa(ip.src)
                    destination_ip_address = socket.inet_ntoa(ip.dst)
                if ip.p in ip_protocol_map:
                    protocols[ip.p] = ip_protocol_map[ip.p]
                # if ip ttl exceeded:
                #     intermediate_ip_addresses.append(socket.inet_ntoa(ip.src))

    return source_ip_address, destination_ip_address, intermediate_ip_addresses, protocols
