from typing import Dict, List
from statistics import mean, pstdev

DECIMAL_PLACES = 2

def print_results(source_node_ip_address: str,
                  ultimate_destination_ip_address: str,
                  intermediate_ip_addresses: List[str],
                  protocols: Dict[int, str],
                  datagrams,
                  round_trip_times: Dict[str, List[float]]) -> None:
    """
    Prints details of a parsed traceroute file, such as IP addresses and protocols
    """
    print(f"The IP address of the source node: {source_node_ip_address}")
    print(f"The IP address of ultimate destination node: {ultimate_destination_ip_address}")
    print("The IP addresses of the intermediate destination nodes:")
    for i, address in enumerate(intermediate_ip_addresses):
        if i == len(intermediate_ip_addresses) - 1:
            print(f"\trouter {i + 1}:\t{address}.")
        else:
            print(f"\trouter {i + 1}:\t{address},")
    print("\nThe values in the protocol field of IP headers:")
    for key in sorted(protocols.keys()):
        print(f"\t{key}:\t{protocols[key]}")
    for fragment_id, fragment in datagrams.items():
        print(f"\nThe number of fragments created from the original datagram "
            f"{fragment_id} is: {fragment.count}")
        print(f"The offset of the last fragment is: {fragment.offset}")
    print("")
    for destination_ip_address, rtts in round_trip_times.items():
        print(f"The avg RRT between {source_node_ip_address} and {destination_ip_address} is: "
            f"{round(mean(rtts) * 1000, DECIMAL_PLACES)} ms, "
            f"the s.d. is: {round(pstdev(rtts) * 1000, DECIMAL_PLACES)} ms")
