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
        protocols = {}
        max_ttl = 0
        source_node_ip_address = ""
        ultimate_destination_node_ip_address = ""
        intermediate_ip_addresses = []
        intermediate_ip_addresses_set = set()
        outgoing_packets = {}
        ttl_counts = [0] * 100
        # how many probes used "per ttl"
        ttl_probe_count = 0
        datagrams = {}
        fragment_id_map = {}

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            # Filter out non IP packets
            if type(ip) is not dpkt.ip.IP:
                continue

            # Add protocol to set
            if ip.p in ip_protocol_map:
                protocols[ip.p] = ip_protocol_map[ip.p]
            else:
                protocols[ip.p] = "Unknown protocol"

            source_ip_address = socket.inet_ntoa(ip.src)
            destination_ip_address = socket.inet_ntoa(ip.dst)
            current_ttl = ip.ttl

            if current_ttl == max_ttl + 1 and is_valid(ip.data):
                max_ttl = current_ttl
                if current_ttl == 1:
                    source_node_ip_address = source_ip_address
                    ultimate_destination_node_ip_address = destination_ip_address

            if current_ttl == 1 and max_ttl == 1 and is_valid(ip.data):
                ttl_probe_count += 1

            # from source node
            if (source_ip_address == source_node_ip_address and
                destination_ip_address == ultimate_destination_node_ip_address and
                current_ttl <= max_ttl + 1):
                fragment_id = ip.id
                frag_offset = 8 * (ip.off & dpkt.ip.IP_OFFMASK)
                if fragment_id not in datagrams:
                    datagrams[fragment_id] = {
                        'count': 0,
                        'offset': 0,
                        'send_times': []
                    }
                if mf_flag_set(ip) or frag_offset > 0:
                    datagrams[fragment_id]['count'] += 1
                    datagrams[fragment_id]['offset'] = frag_offset
                datagrams[fragment_id]['send_times'].append(ts)

                intermediate_ip_addresses.append("") # placeholder to be filled in
                intermediate_ip_addresses.append("") # placeholder to be filled in
                intermediate_ip_addresses.append("") # placeholder to be filled in
                intermediate_ip_addresses.append("") # placeholder to be filled in
                intermediate_ip_addresses.append("") # placeholder to be filled in

                key = -1
                if is_udp(ip.data):
                    key = ip.data.dport
                elif is_icmp(ip.data, 8):
                    key = ip.data['echo'].seq
                if key != -1:
                    fragment_id_map[key] = fragment_id
                    outgoing_packets[key] = {
                        'ttl': ip.ttl,
                        'ttl_adj': ttl_counts[ip.ttl]
                    }
                    ttl_counts[ip.ttl] += 1

            elif destination_ip_address == source_node_ip_address and is_icmp(ip.data):
                icmp = ip.data
                icmp_type = icmp.type
                data_packet = icmp.data
                if icmp_type == 0 or icmp_type == 8:
                    # handle ping reply case
                    seq = data_packet.seq
                    outgoing_packets[seq]['reply_time'] = ts
                    outgoing_packets[seq]['ip'] = source_ip_address
                    outgoing_packets[seq]['fragment_id'] = fragment_id_map[seq]
                    continue

                data_packet = icmp.data.data.data

                if is_udp(data_packet):
                    key = data_packet.dport
                elif is_icmp(data_packet):
                    key = data_packet['echo'].seq
                if key in outgoing_packets:
                    outgoing_packets[key]['reply_time'] = ts
                    outgoing_packets[key]['ip'] = source_ip_address
                    outgoing_packets[key]['fragment_id'] = fragment_id_map[key]
                    if icmp_type == 11 and source_ip_address not in intermediate_ip_addresses_set:
                        ttl = outgoing_packets[key]['ttl']
                        ttl_adj = outgoing_packets[key]['ttl_adj']
                        intermediate_ip_addresses[(ttl * 5) - 1 + ttl_adj] = source_ip_address
                        intermediate_ip_addresses_set.add(source_ip_address)

    # remove empty strings from ip list (packets sent out which didn't return from an intermediate host)
    while "" in intermediate_ip_addresses: intermediate_ip_addresses.remove("")

    return (source_node_ip_address,
            ultimate_destination_node_ip_address,
            list(intermediate_ip_addresses),
            protocols,
            0,
            0)

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
