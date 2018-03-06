#!/usr/bin/env python3
"""
University of Victoria
Spring 2018
CSC 361 Assignment 3
Michael Reiter
V00831568
"""

import argparse
from traceroute.results_logger import print_results

def main() -> None:
    """
    Analyzes the trace of IP datagrams created by traceroute
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("address")
    args = parser.parse_args()
    print_results()

if __name__ == "__main__":
    main()
