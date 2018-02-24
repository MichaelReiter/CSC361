class TCPConnection:
    """
    A TCP connection parsed from an input trace file.
    Uniquely identified by the 4 tuple
    (source IP address, source port, destination IP address, destination port).
    """
    def __init__(self) -> None:
        self.source_ip_address: str = None
        self.destination_ip_address: str = None
        self.source_port: int = None
        self.destination_port: int = None
        self.start_time: float = 0
        self.end_time: float = 0

    def get_duration(self) -> float:
        """
        Computes time TCP connection was open
        """
        return self.end_time - self.start_time


def compute_round_trip_time(connection: TCPConnection) -> float:
    """
    Returns round trip time (RTT) of a TCP connection in milliseconds
    """
    return 0
