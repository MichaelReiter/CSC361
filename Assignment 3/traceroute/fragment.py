class DatagramFragment(object):
    """
    A UDP or ICMP packet
    """
    def __init__(self):
        self.count = 0
        self.offset = 0
        self.send_times = []
