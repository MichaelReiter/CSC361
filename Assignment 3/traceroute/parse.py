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
        intermediate_ip_addresses = set()
        protocols = {}
        test = []
        number_of_fragments = 1
        last_fragment_offset = 0
        source_ip_address = ""
        first_packet_id = 0
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            # Filter out non IP packets
            if type(ip) == dpkt.ip.IP:
                if first_packet_id == 0 and ip.ttl == 1:
                    source_ip_address = socket.inet_ntoa(ip.src)
                    destination_ip_address = socket.inet_ntoa(ip.dst)
                    first_packet_id = ip.id
                if ip.p in ip_protocol_map:
                    protocols[ip.p] = ip_protocol_map[ip.p]
                else:
                    protocols[ip.p] = "Unknown protocol"
                test.append(ip)
                # TTL exceeded: add intermediate (hop) IP address
                if type(ip.data) == dpkt.icmp.ICMP and ip.data.type == 11:
                    intermediate_ip_addresses.add(socket.inet_ntoa(ip.src))
                if socket.inet_ntoa(ip.src) == source_ip_address:
                    if ip.mf == 1:
                        number_of_fragments += 1
                    else:
                        last_fragment_offset = ip.off

    return (source_ip_address,
            destination_ip_address,
            list(intermediate_ip_addresses),
            protocols,
            number_of_fragments,
            last_fragment_offset)
