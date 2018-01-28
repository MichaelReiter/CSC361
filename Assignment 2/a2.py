'''
For each TCP connection, your program needs to provide the following
statistical results for the whole trace data:
- the number of reset TCP connections observed in the trace
- the number of TCP connections that were still open when the trace capture ended
- the number of complete TCP connections observed in the trace

Regarding the complete TCP connections you observed:
- the minimum, mean, and maximum time durations of the complete TCP connections
– the minimum, mean, and maximum RTT (Round Trip Time) values of the complete TCP connections
– the minimum, mean, and maximum number of packets (both directions) sent on the complete TCP connections
– the minimum, mean, and maximum receive window sizes (both sides) of the complete TCP connections.
'''

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
    connections = []
    for i, connection in enumerate(connections):
        print("Connection " + str(i + 1) + ": ")
        print_connection_details(connection)
        print("+++++++++++++++++++++++++++++++++")
    
    print("Total number of complete TCP connections: ")
    print("Number of reset TCP connections: ")
    print("Number of TCP connections that were still open when the trace capture ended: \n")

    print("Minimum time durations: ")
    print("Mean time durations: ")
    print("Maximum time durations: \n")

    print("Minimum RTT values including both send/received: ")
    print("Mean RTT values including both send/received: ")
    print("Maximum RTT values including both send/received: \n")

    print("Minimum number of packets including both send/received: ")
    print("Mean number of packets including both send/received: ")
    print("Maximum number of packets including both send/received: \n")

    print("Minimum receive window sizes including both send/received: ")
    print("Mean receive window sizes including both send/received: ")
    print("Maximum receive window sizes including both send/received: ")


if __name__ == "__main__":
    main()
