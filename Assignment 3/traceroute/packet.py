class Packet(object):
    """
    Represents a data packet identified by fragment_id, 
    originating from source_ip_address, sent at timestamp
    """
    def __init__(self) -> None:
        self.fragment_id = 0
        self.source_ip_address = ""
        self.timestamp = 0
        self.ttl = 0
        self.ttl_adj = 0
