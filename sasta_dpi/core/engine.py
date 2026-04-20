import abc
from sasta_dpi.core.session import PacketConfig

class Response:
    def __init__(self, raw_data: bytes, summary: str, status: str, latency: float):
        self.raw_data = raw_data
        self.summary = summary
        self.status = status # "Open", "Closed", "Filtered", "Success", "Error"
        self.latency = latency

class BaseEngine(abc.ABC):
    @abc.abstractmethod
    async def send(self, config: PacketConfig) -> Response:
        """Send a single packet according to config and return Response"""
        pass
        
    @abc.abstractmethod
    def build_packet(self, config: PacketConfig):
        """Construct the raw packet/query representation."""
        pass
