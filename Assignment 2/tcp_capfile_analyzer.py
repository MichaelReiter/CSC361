#!/usr/bin/env python3
"""
University of Victoria
Spring 2018
CSC 361 Assignment 2
Michael Reiter
V00831568
"""

import argparse
from tcp.connection import TCPConnection
from tcp.capture_parsing import read_cap_file
from tcp.connections_logger import (print_complete_tcp_connections,
                                    print_connection_details,
                                    print_general,
                                    print_total_connections)
from typing import List

def main() -> None:
    """
    Analyses a TCP trace file and prints information about its connections
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("capfile")
    args = parser.parse_args()
    connections: List[TCPConnection] = read_cap_file(args.capfile)
    print_total_connections(connections)
    print_connection_details(connections)
    print_general(connections)
    print_complete_tcp_connections(connections)

if __name__ == "__main__":
    main()
