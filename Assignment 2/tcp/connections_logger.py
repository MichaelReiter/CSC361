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
    for i, connection in enumerate(connections):
        print(f"Connection {i + 1}:")
        print(f"Source Address: {connection.source_ip_address}")
        print(f"Destination address: {connection.destination_ip_address}")
        print(f"Source Port: {connection.source_port}")
        print(f"Destination Port: {connection.destination_port}")
        print(f"Status: {connection.status}")
        # Only if the connection is complete provide the following information
        print(f"Start time: {connection.start_time}")
        print(f"End Time: {connection.end_time}")
        print(f"Duration: {connection.duration}")
        print(f"Number of packets sent from Source to Destination: {None}")
        print(f"Number of packets sent from Destination to Source: {None}")
        print(f"Total number of packets: {None}")
        print(f"Number of data bytes sent from Source to Destination: {None}")
        print(f"Number of data bytes sent from Destination to Source: {None}")
        print(f"Total number of data bytes: {None}")
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
    complete = [c for c in connections if c.syn_count > 0 and c.fin_count > 0]
    print(f"Total number of complete TCP connections: {len(complete)}")
    reset = [c for c in connections if c.rst_count > 0]
    print(f"Number of reset TCP connections: {len(reset)}\n")
    # open = [c for c in connections if c]
    # print(f"Number of TCP connections that were still open when the trace capture ended:
    #     {len(open)}\n")
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
