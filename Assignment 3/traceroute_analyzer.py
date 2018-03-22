#!/usr/bin/env python3
"""
University of Victoria
Spring 2018
CSC 361 Assignment 3
Michael Reiter
V00831568
"""

import argparse
from traceroute.parse import read_trace_file
from traceroute.results_logger import print_results

def main() -> None:
    """
    Analyzes the trace of IP datagrams created by traceroute
    """
    # parser = argparse.ArgumentParser()
    # parser.add_argument("tracefile")
    # args = parser.parse_args()
    results = read_trace_file("/Users/michael/Dropbox/Programming/361/Assignment 3/traces/trace1.pcapng")
    print_results(*results)

if __name__ == "__main__":
    main()
