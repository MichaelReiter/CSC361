'''
University of Victoria
Spring 2018
CSC 361 Assignment 2
Michael Reiter
V00831568
'''

import argparse
import dpkt
import pcapy
from typing import BinaryIO, List

class TCPConnection:
    '''
    A TCP connection parsed from an input trace file.
    Uniquely identified by the 4 tuple
    (source IP address, source port, destination IP address, destination port).
    '''
    def __init__(self) -> None:
        self.source_ip_address: str = None
        self.destination_ip_address: str = None
        self.source_port: int = None
        self.destination_port: int = None
        self.start_time: float = 0
        self.end_time: float = 0

    def get_duration(self) -> float:
        '''
        Computes time TCP connection was open
        '''
        return self.end_time - self.start_time


def compute_round_trip_time(connection: TCPConnection) -> float:
    '''
    Computes round trip time (RTT) of a TCP connection
    '''
    return 0


def print_total_connections(connections: List[TCPConnection]) -> None:
    '''
    Prints total number of connections
    '''
    print(f"Total number of connections: {None}")


def print_connection_details(connections: List[TCPConnection]) -> None:
    '''
    Prints statistical information about TCP connections
    '''
    for i, connection in enumerate(connections):
        print(f"Connection {i + 1}:")
        print(f"Source Address: {connection.source_ip_address}")
        print(f"Destination address: {connection.destination_ip_address}")
        print(f"Source Port: {connection.source_port}")
        print(f"Destination Port: {connection.destination_port}")
        print(f"Status: {None}")
        # Only if the connection is complete provide the following information
        print(f"Start time: {connection.start_time}")
        print(f"End Time: {connection.end_time}")
        print(f"Duration: {connection.get_duration()}")
        print(f"Number of packets sent from Source to Destination: {None}")
        print(f"Number of packets sent from Destination to Source: {None}")
        print(f"Total number of packets: {None}")
        print(f"Number of data bytes sent from Source to Destination: {None}")
        print(f"Number of data bytes sent from Destination to Source: {None}")
        print(f"Total number of data bytes: {None}")
        print("END")
        print("+++++++++++++++++++++++++++++++++")


def read_cap_file(filename: str) -> List[TCPConnection]:
    '''
    Returns connections parsed from a TCP trace file
    '''
    f: BinaryIO = open(filename, "rb")
    pcap: dpkt.pcap.Reader = dpkt.pcap.Reader(f)

    connections: List[TCPConnection] = []
    for ts, buf in pcap:
        eth: dpkt.ethernet.Ethernet = dpkt.ethernet.Ethernet(buf)
        ip: dpkt.ip.IP = eth.data
        tcp: dpkt.tcp.TCP = ip.data

        if tcp.dport == 80 and len(tcp.data) > 0:
            http: dpkt.http.Request = dpkt.http.Request(tcp.data)
            # print(http.uri)

    return connections


def print_general(connections: List[TCPConnection]) -> None:
    '''
    Prints statistical information about complete, reset and open TCP connections
    '''
    print(f"Total number of complete TCP connections: {None}")
    print(f"Number of reset TCP connections: {None}")
    print(f"Number of TCP connections that were still open when the trace capture ended: {None}\n")


def print_complete_tcp_connections(connections: List[TCPConnection]):
    '''
    Prints statistical information about TCP connection duration,
    round trip time, packets and window size
    '''
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


def main() -> None:
    '''
    Analyses a TCP trace file and prints information about its connections
    '''
    # parser = argparse.ArgumentParser()
    # parser.add_argument("capfile")
    # args = parser.parse_args()
    connections: List[TCPConnection] = read_cap_file(
        "/Users/michael/Dropbox/Programming/361/Assignment 2/sample-capture-file")
    # print_total_connections(connections)
    # print_connection_details(connections)
    # print_general(connections)
    # print_complete_tcp_connections(connections)


if __name__ == "__main__":
    main()
