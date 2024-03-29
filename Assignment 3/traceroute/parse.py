import dpkt
import re
import socket
import sys
from traceroute.fragment import DatagramFragment
from traceroute.ip_protocols import ip_protocol_map
from traceroute.packet import Packet
from traceroute.results_logger import print_results
from typing import Dict, List

def read_trace_file(filename: str) -> (str, str, List[str], Dict[int, str]):
    """
    Returns source IP, destination IP, intermediate IPs
    and protocols parsed from a trace file
    """
    with open(filename, "rb") as f:
        # Handle pcap and pcapng input filetype
        if re.match(r"^.*\.(pcap)$", filename):
            pcap = dpkt.pcap.Reader(f)
        elif re.match(r"^.*\.(pcapng)$", filename):
            pcap = dpkt.pcapng.Reader(f)
        else:
            print("Failed to read pcap or pcapng. Exiting.")
            sys.exit()

        protocols = {}
        packets = {}
        fragments = {}
        fragment_ids = {}
        max_ttl = 0
        source_node_ip_address = ""
        ultimate_destination_node_ip_address = ""
        intermediate_ip_addresses = []
        ttls = [0] * 1024

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            # Filter out non IP packets
            if type(ip) is not dpkt.ip.IP:
                continue

            # Update protocol set
            if ip.p in ip_protocol_map:
                protocols[ip.p] = ip_protocol_map[ip.p]
            else:
                protocols[ip.p] = "Unknown protocol"

            source_ip_address = socket.inet_ntoa(ip.src)
            destination_ip_address = socket.inet_ntoa(ip.dst)

            # Set source node and ultimate destination IP addresses
            if ip.ttl == max_ttl + 1 and is_valid(ip.data):
                max_ttl = ip.ttl
                if ip.ttl == 1:
                    source_node_ip_address = source_ip_address
                    ultimate_destination_node_ip_address = destination_ip_address

            if (source_ip_address == source_node_ip_address and
                destination_ip_address == ultimate_destination_node_ip_address and
                ip.ttl <= max_ttl + 1):
                fragment_id = ip.id
                fragment_offset = 8 * (ip.off & dpkt.ip.IP_OFFMASK)
                if fragment_id not in fragments:
                    fragments[fragment_id] = DatagramFragment()
                if mf_flag_set(ip) or fragment_offset > 0:
                    fragments[fragment_id].count += 1
                    fragments[fragment_id].offset = fragment_offset
                fragments[fragment_id].send_times.append(ts)

                for i in range(5):
                    intermediate_ip_addresses.append("")

                key = -1
                if is_udp(ip.data):
                    key = ip.data.dport
                elif is_icmp(ip.data, 8):
                    key = ip.data["echo"].seq
                if key != -1:
                    fragment_ids[key] = fragment_id
                    packets[key] = Packet()
                    packets[key].ttl = ip.ttl
                    packets[key].ttl_adj = ttls[ip.ttl]
                    ttls[ip.ttl] += 1

            elif destination_ip_address == source_node_ip_address and is_icmp(ip.data):
                icmp_type = ip.data.type
                if icmp_type == 0 or icmp_type == 8:
                    packets[ip.data.data.seq].timestamp = ts
                    packets[ip.data.data.seq].source_ip_address = source_ip_address
                    packets[ip.data.data.seq].fragment_id = fragment_ids[ip.data.data.seq]
                    continue

                packet_data = ip.data.data.data.data

                if is_udp(packet_data):
                    key = packet_data.dport
                elif is_icmp(packet_data):
                    key = packet_data["echo"].seq
                if key in packets:
                    packets[key].timestamp = ts
                    packets[key].source_ip_address = source_ip_address
                    packets[key].fragment_id = fragment_ids[key]
                    if icmp_type == 11 and source_ip_address not in set(intermediate_ip_addresses):
                        ttl = packets[key].ttl
                        ttl_adj = packets[key].ttl_adj
                        intermediate_ip_addresses[(5 * ttl) - 1 + ttl_adj] = source_ip_address

    intermediate_ip_addresses = [ip for ip in intermediate_ip_addresses if ip != ""]
    round_trip_times = compute_round_trip_times(packets.values(), fragments)

    return (source_node_ip_address,
            ultimate_destination_node_ip_address,
            intermediate_ip_addresses,
            protocols,
            fragments,
            round_trip_times)

def compute_round_trip_times(packets: List[Packet],
                             fragments: Dict[int, DatagramFragment]) -> Dict[str, List[float]]:
    """
    Calculates round trip times for packets (in seconds)
    """
    round_trip_times = {}
    for packet in packets:
        if packet.fragment_id == 0 or packet.timestamp == 0:
            continue
        fragment_id = packet.fragment_id
        timestamp = packet.timestamp
        source_ip_address = packet.source_ip_address
        send_times = fragments[fragment_id].send_times
        if source_ip_address not in round_trip_times:
            round_trip_times[source_ip_address] = []
        for time in send_times:
            round_trip_times[source_ip_address].append(timestamp - time)
    return round_trip_times

def mf_flag_set(ip: dpkt.ip.IP) -> bool:
    """
    Returns boolean indicating if IP packet has more fragments
    """
    return bool(ip.off & dpkt.ip.IP_MF)

def is_udp(data) -> bool:
    """
    Returns boolean indicating if data is UDP
    """
    return type(data) is dpkt.udp.UDP

def is_icmp(data, icmp_type=None) -> bool:
    """
    Returns boolean indicating if data is ICMP and given type
    """
    if icmp_type is not None:
        return type(data) is dpkt.icmp.ICMP and data.type == icmp_type
    else:
        return type(data) is dpkt.icmp.ICMP

def is_valid(data) -> bool:
    """
    Returns boolean indicating if data is UDP or ICMP type 8
    """
    return is_udp(data) or is_icmp(data, 8)
