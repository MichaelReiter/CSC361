from tcp.connection import TCPConnection
from typing import List

DECIMAL_PLACES = 5

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
    global_start_time = min(c.start_time for c in connections)
    for i, connection in enumerate(connections):
        print(f"Connection {i + 1}:")
        print(f"Source Address: {connection.source_ip_address}")
        print(f"Destination address: {connection.destination_ip_address}")
        print(f"Source Port: {connection.source_port}")
        print(f"Destination Port: {connection.destination_port}")
        print(f"Status: {connection.status}")
        if connection.is_complete:
            print(f"Start time: "
                f"{round(abs(global_start_time - connection.start_time), DECIMAL_PLACES)}")
            print(f"End Time: "
                f"{round(abs(global_start_time - connection.end_time), DECIMAL_PLACES)}")
            print(f"Duration: {round(connection.duration, DECIMAL_PLACES)}")
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
    complete = [c for c in connections if c.is_complete]
    print(f"Total number of complete TCP connections: {len(complete)}")
    reset = [c for c in connections if c.rst_count > 0]
    print(f"Number of reset TCP connections: {len(reset)}")
    incomplete = [c for c in connections if not c.is_complete]
    print(f"Number of TCP connections that were still open when the trace capture ended: "
        f"{len(incomplete)}\n")
    print("--------------------------------------------------------------------------\n")


def print_complete_tcp_connections(connections: List[TCPConnection]) -> None:
    """
    Prints statistical information about TCP connection duration,
    round trip time, packets and window size
    """
    print("D) Complete TCP connections:\n")
    durations = [c.duration for c in connections if c.is_complete]
    min_duration = min(durations)
    mean_duration = sum(durations) / len(durations)
    max_duration = max(durations)
    print(f"Minimum time duration: {round(min_duration, DECIMAL_PLACES)}")
    print(f"Mean time duration: {round(mean_duration, DECIMAL_PLACES)}")
    print(f"Maximum time duration: {round(max_duration, DECIMAL_PLACES)}\n")
    round_trip_times = []
    for c in connections:
        if c.is_complete:
            for rtt in c.round_trip_times:
                round_trip_times.append(rtt)
    min_round_trip_time = min(round_trip_times)
    mean_round_trip_time = sum(round_trip_times) / len(round_trip_times)
    max_round_trip_time = max(round_trip_times)
    print(f"Minimum RTT value: {round(min_round_trip_time, DECIMAL_PLACES)}")
    print(f"Mean RTT value: {round(mean_round_trip_time, DECIMAL_PLACES)}")
    print(f"Maximum RTT value: {round(max_round_trip_time, DECIMAL_PLACES)}\n")
    packets = [c.total_packets for c in connections if c.is_complete]
    min_packets = min(packets)
    mean_packets = sum(packets) / len(packets)
    max_packets = max(packets)
    print(f"Minimum number of packets including both send/received: {min_packets}")
    print(f"Mean number of packets including both send/received: "
        f"{round(mean_packets, DECIMAL_PLACES)}")
    print(f"Maximum number of packets including both send/received: {max_packets}\n")
    receive_windows = []
    for c in connections:
        if c.is_complete:
            for window_size in c.receive_windows:
                receive_windows.append(window_size)
    min_receive_windows = min(receive_windows)
    mean_receive_windows = sum(receive_windows) / len(receive_windows)
    max_receive_windows = max(receive_windows)
    print(f"Minimum receive window size including both send/received: {min_receive_windows}")
    print(f"Mean receive window size including both send/received: "
        f"{round(mean_receive_windows, DECIMAL_PLACES)}")
    print(f"Maximum receive window size including both send/received: {max_receive_windows}\n")
    print("--------------------------------------------------------------------------\n")    
