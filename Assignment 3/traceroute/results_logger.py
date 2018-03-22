from typing import Dict, List

def print_results(source_ip_address: str,
                  destination_ip_address: str,
                  intermediate_ip_addresses: List[str],
                  protocols: Dict[int, str]) -> None:
    """
    Prints details of a parsed traceroute file, such as IP addresses and protocols
    """
    print(f"The IP address of the source node: {source_ip_address}")
    print(f"The IP address of ultimate destination node: {destination_ip_address}")
    print("The IP addresses of the intermediate destination nodes:")
    for i, address in enumerate(intermediate_ip_addresses):
        if i == len(intermediate_ip_addresses - 1):
            print(f"\trouter {i + 1}: {address}.")
        else:
            print(f"\trouter {i + 1}: {address},")
    print("The values in the protocol field of IP headers:")
    for key in sorted(protocols.keys()):
        print(f"\t{key}: {protocols[key]}")
    # print(f"The number of fragments created from the original datagram is: {None}")
    # print(f"The offset of the last fragment is: {None}")
    # print(f"The avg RRT between {None} and {None} is: {None} ms, the s.d. is: {None} ms")
