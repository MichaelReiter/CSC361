from typing import Dict, List

def print_results(source_ip_address: str,
                  destination_ip_address: str,
                  intermediate_ip_addresses: List[str],
                  protocols: Dict[int, str],
                  number_of_fragments: int,
                  last_fragment_offset: int) -> None:
    """
    Prints details of a parsed traceroute file, such as IP addresses and protocols
    """
    print(f"The IP address of the source node: {source_ip_address}")
    print(f"The IP address of ultimate destination node: {destination_ip_address}")
    print("The IP addresses of the intermediate destination nodes:")
    for i, address in enumerate(intermediate_ip_addresses):
        if i == len(intermediate_ip_addresses) - 1:
            print(f"\trouter {i + 1}:\t{address}.")
        else:
            print(f"\trouter {i + 1}:\t{address},")
    # print("\nThe values in the protocol field of IP headers:")
    # for key in sorted(protocols.keys()):
    #     print(f"\t{key}:\t{protocols[key]}")
    # print(f"\nThe number of fragments created from the original datagram is: "
    #     f"{number_of_fragments}")
    # print(f"The offset of the last fragment is: {last_fragment_offset}\n")
    # for address in intermediate_ip_addresses:
    #     rtt = 0
    #     stdev = 0
    #     print(f"The avg RRT between {source_ip_address} and {address} is: {rtt} ms, "
    #         f"the s.d. is: {stdev} ms")
