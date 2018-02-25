from operator import attrgetter
from tcp.connection import TCPConnection
from typing import List

def print_total_connections(connections: List[TCPConnection]) -> None:
    """
    Prints total number of connections
    """
    print(f"A) Total number of connections: {len(connections)}\n")
    print("--------------------------------------------------------------------------\n")


def print_connection_details(connections: List[TCPConnection]) -> None:
    """
    Prints statistical information about TCP connections
    """
    print("B) Connections' details:\n")
    global_start_time = min(connections, key=attrgetter("start_time")).start_time
    for i, connection in enumerate(connections):
        print(f"Connection {i + 1}:")
        print(f"Source Address: {connection.source_ip_address}")
        print(f"Destination address: {connection.destination_ip_address}")
        print(f"Source Port: {connection.source_port}")
        print(f"Destination Port: {connection.destination_port}")
        print(f"Status: {connection.status}")
        if connection.complete:
            print(f"Start time: {round(abs(global_start_time - connection.start_time), 5)}")
            print(f"End Time: {round(abs(global_start_time - connection.end_time), 5)}")
            print(f"Duration: {round(connection.duration, 5)}")
            print(f"Number of packets sent from Source to Destination: "
                f"{connection.packets_source_to_destination}")
            print(f"Number of packets sent from Destination to Source: "
                f"{connection.packets_destination_to_source}")
            print(f"Total number of packets: {connection.total_packets}")
            print(f"Number of data bytes sent from Source to Destination: "
                f"{connection.bytes_source_to_destination}")
            print(f"Number of data bytes sent from Destination to Source: "
                f"{connection.bytes_destination_to_source}")
            print(f"Total number of data bytes: {connection.total_bytes}")
        print("END")
        if i + 1 != len(connections):
            print("+++++++++++++++++++++++++++++++++")
    print()
    print("--------------------------------------------------------------------------\n")


def print_general(connections: List[TCPConnection]) -> None:
    """
    Prints statistical information about complete, reset and open TCP connections
    """
    print("C) General\n")
    complete = [c for c in connections if c.complete]
    print(f"Total number of complete TCP connections: {len(complete)}")
    reset = [c for c in connections if c.rst_count > 0]
    print(f"Number of reset TCP connections: {len(reset)}")
    open = [c for c in connections if not c.complete]
    print(f"Number of TCP connections that were still open when the trace capture ended: "
        f"{len(open)}\n")
    print("--------------------------------------------------------------------------\n")


def print_complete_tcp_connections(connections: List[TCPConnection]) -> None:
    """
    Prints statistical information about TCP connection duration,
    round trip time, packets and window size
    """
    print("D) Complete TCP connections:\n")
    print(f"Minimum time duration: {None}")
    print(f"Mean time duration: {None}")
    print(f"Maximum time duration: {None}\n")
    print(f"Minimum RTT value: {None}")
    print(f"Mean RTT value: {None}")
    print(f"Maximum RTT value: {None}\n")
    print(f"Minimum number of packets including both send/received: {None}")
    print(f"Mean number of packets including both send/received: {None}")
    print(f"Maximum number of packets including both send/received: {None}\n")
    print(f"Minimum receive window size including both send/received: {None}")
    print(f"Mean receive window size including both send/received: {None}")
    print(f"Maximum receive window size including both send/received: {None}\n")
    print("--------------------------------------------------------------------------\n")    
