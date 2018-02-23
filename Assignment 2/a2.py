# University of Victoria
# Spring 2018
# CSC 361 Assignment 2
# Michael Reiter
# V00831568

import argparse
import pcapy

class TCPConnection:
    '''
    A TCP connection parsed from an input trace file
    '''
    def __init__(self):
        self.source_address = None
        self.destination_address = None
        self.source_port = None
        self.destination_port = None
        self.start_time = None
        self.end_time = None

    def get_duration(self):
        '''
        Computes time TCP connection was open
        '''
        return self.end_time - self.start_time


def compute_rtt():
    '''
    Computes round trip time (RTT) of a TCP connection
    '''
    return 0


def print_connection_details(connection):
    '''
    Prints information about a TCP connection.
    '''
    print("Source Address: " + connection.source_address)
    print("Destination address: " + connection.destination_address)
    print("Source Port: " + connection.source_port)
    print("Destination Port: " + connection.destination_port)
    print("Status: ")
    # Only if the connection is complete provide the following information
    print("Start time: " + connection.start_time)
    print("End Time: " + connection.end_time)
    print("Duration: " + connection.get_duration())
    print("Number of packets sent from Source to Destination: ")
    print("Number of packets sent from Destination to Source: ")
    print("Total number of packets: ")
    print("Number of data bytes sent from Source to Destination: ")
    print("Number of data bytes sent from Destination to Source: ")
    print("Total number of data bytes: ")
    print("END")


def main():
    '''
    Analyses a TCP trace file.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("capfile")
    args = parser.parse_args()
    # print(args.capfile)

    connections = []
    for i, connection in enumerate(connections):
        print("Connection " + str(i + 1) + ":")
        print_connection_details(connection)
        print("+++++++++++++++++++++++++++++++++")

    # print("Total number of complete TCP connections: " + )
    # print("Number of reset TCP connections: " + )
    # print("Number of TCP connections that were still open when the trace capture ended: " + __ + "\n")

    # print("Minimum time duration: " + )
    # print("Mean time duration: " + )
    # print("Maximum time duration: " + __ + "\n")

    # print("Minimum RTT value: " + )
    # print("Mean RTT value: " + )
    # print("Maximum RTT value: " + __ + "\n")

    # print("Minimum number of packets including both send/received: " + )
    # print("Mean number of packets including both send/received: " + )
    # print("Maximum number of packets including both send/received: " + __ + "\n")

    # print("Minimum receive window size including both send/received: " + )
    # print("Mean receive window size including both send/received: " + )
    # print("Maximum receive window size including both send/received: " + )


if __name__ == "__main__":
    main()
