"""
University of Victoria
Spring 2018
CSC 361 Assignment 2
Michael Reiter
V00831568
"""

import argparse
from lib.tcp_connection import TCPConnection
from lib.capture_parsing import read_cap_file
from lib.connections_logger import \
    print_complete_tcp_connections, print_connection_details, print_general, print_total_connections
from typing import List

def main() -> None:
    """
    Analyses a TCP trace file and prints information about its connections
    """
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
