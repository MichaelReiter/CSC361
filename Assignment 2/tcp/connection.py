from typing import List

class TCPConnection(object):
    """
    A TCP connection parsed from an input trace file.
    Uniquely identified by the 4 tuple
    (source IP address, source port, destination IP address, destination port).
    """
    def __init__(self,
                 source_ip_address: str,
                 destination_ip_address: str,
                 source_port: int,
                 destination_port: int) -> None:
        self.source_ip_address: str = source_ip_address
        self.destination_ip_address: str = destination_ip_address
        self.source_port: int = source_port
        self.destination_port: int = destination_port
        self.start_time: float = float("inf")
        self.end_time: float = -float("inf")
        self.syn_count: int = 0
        self.ack_count: int = 0
        self.fin_count: int = 0
        self.rst_count: int = 0
        self.packets_source_to_destination: int = 0
        self.packets_destination_to_source: int = 0
        self.bytes_source_to_destination: int = 0
        self.bytes_destination_to_source: int = 0
        self.round_trip_times: List[float] = []
        self.receive_windows: List[int] = []

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            ips_match = (set([self.source_ip_address, self.destination_ip_address]) ==
                set([other.source_ip_address, other.destination_ip_address]))
            ports_match = (set([self.source_port, self.destination_port]) ==
                set([other.source_port, other.destination_port]))
            return ips_match and ports_match
        return False

    def __hash__(self):
        return (hash(self.source_ip_address) ^
                hash(self.destination_ip_address) ^
                hash(self.source_port) ^
                hash(self.destination_port))

    @property
    def duration(self) -> float:
        """
        Time TCP connection was open in milliseconds
        """
        return self.end_time - self.start_time

    @property
    def status(self) -> str:
        """
        String encoding SYN and FIN counts
        """
        return f"S{self.syn_count}F{self.fin_count}"

    @property
    def is_complete(self) -> bool:
        """
        A connection is considered complete if it has at least 1 SYN and 1 ACK
        """
        return self.syn_count > 0 and self.fin_count > 0

    @property
    def total_packets(self) -> int:
        """
        Number of packets sent between source and destination
        """
        return self.packets_source_to_destination + self.packets_destination_to_source

    @property
    def total_bytes(self) -> int:
        """
        Number of bytes sent between source and destination
        """
        return self.bytes_source_to_destination + self.bytes_destination_to_source

    def compute_round_trip_time(self) -> float:
        """
        Returns round trip time (RTT) of a TCP connection in milliseconds
        """
        return 0
