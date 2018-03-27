import dpkt
import socket
from traceroute.fragment import DatagramFragment
from traceroute.ip_protocols import ip_protocol_map
from traceroute.results_logger import print_results
from typing import Dict, List

def read_trace_file(filename: str) -> (str, str, List[str], Dict[int, str]):
    """
    Returns source IP, destination IP, intermediate IPs
    and protocols parsed from a trace file
    """
    with open(filename, "rb") as f:
        try:
            pcap = dpkt.pcapng.Reader(f)
        except ValueError:
            pcap = dpkt.pcap.Reader(f)
            print("Switched from reading pcapng files to reading pcap files")
        except Exception:
            print("Failed to read pcapng or pcap. Exiting.")
            sys.exit()
        protocols = {}
        max_ttl = 0
        source_node_ip_address = ""
        ultimate_destination_node_ip_address = ""
        intermediate_ip_addresses = []
        intermediate_ip_addresses_set = set()
        outgoing_packets = {}
        ttl_counts = [0] * 100
        ttl_probe_count = 0
        datagrams = {}
        fragment_ids = {}

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            # Filter out non IP packets
            if type(ip) is not dpkt.ip.IP:
                continue

            if ip.ttl == 1 and max_ttl == 1 and is_valid(ip.data):
                ttl_probe_count += 1

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
                if fragment_id not in datagrams:
                    datagrams[fragment_id] = DatagramFragment()
                if mf_flag_set(ip) or fragment_offset > 0:
                    datagrams[fragment_id].count += 1
                    datagrams[fragment_id].offset = fragment_offset
                datagrams[fragment_id].send_times.append(ts)

                for i in range(5):
                    intermediate_ip_addresses.append("")

                key = -1
                if is_udp(ip.data):
                    key = ip.data.dport
                elif is_icmp(ip.data, 8):
                    key = ip.data['echo'].seq
                if key != -1:
                    fragment_ids[key] = fragment_id
                    outgoing_packets[key] = {
                        'ttl': ip.ttl,
                        'ttl_adj': ttl_counts[ip.ttl]
                    }
                    ttl_counts[ip.ttl] += 1

            elif destination_ip_address == source_node_ip_address and is_icmp(ip.data):
                icmp = ip.data
                icmp_type = icmp.type
                if icmp_type == 0 or icmp_type == 8:
                    outgoing_packets[icmp.data.seq]['timestamp'] = ts
                    outgoing_packets[icmp.data.seq]['ip'] = source_ip_address
                    outgoing_packets[icmp.data.seq]['fragment_id'] = fragment_ids[icmp.data.seq]
                    continue

                data_packet = icmp.data.data.data

                if is_udp(data_packet):
                    key = data_packet.dport
                elif is_icmp(data_packet):
                    key = data_packet['echo'].seq
                if key in outgoing_packets:
                    outgoing_packets[key]['timestamp'] = ts
                    outgoing_packets[key]['ip'] = source_ip_address
                    outgoing_packets[key]['fragment_id'] = fragment_ids[key]
                    if icmp_type == 11 and source_ip_address not in intermediate_ip_addresses_set:
                        ttl = outgoing_packets[key]['ttl']
                        ttl_adj = outgoing_packets[key]['ttl_adj']
                        intermediate_ip_addresses[(ttl * 5) - 1 + ttl_adj] = source_ip_address
                        intermediate_ip_addresses_set.add(source_ip_address)

    while "" in intermediate_ip_addresses:
        intermediate_ip_addresses.remove("")

    round_trip_times = {}
    for _, packet in outgoing_packets.items():
        if 'fragment_id' not in packet:
            continue
        fragment_id = packet['fragment_id']
        send_times = datagrams[fragment_id].send_times
        if 'timestamp' not in packet:
            continue
        timestamp = packet['timestamp']
        ip = packet['ip']
        if ip not in round_trip_times:
            round_trip_times[ip] = []
        for sent in send_times:
            round_trip_times[ip].append(timestamp - sent)

    return (source_node_ip_address,
            ultimate_destination_node_ip_address,
            list(intermediate_ip_addresses),
            protocols,
            datagrams,
            round_trip_times)

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
