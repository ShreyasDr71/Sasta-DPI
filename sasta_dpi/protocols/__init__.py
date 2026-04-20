from .tcp import TCPEngine
from .http import HttpEngine
from .dns import DnsEngine
from .udp import UDPEngine
from .icmp import ICMPEngine
from .arp import ARPEngine

def get_engine(protocol: str):
    proto_map = {
        "tcp": TCPEngine,
        "http": HttpEngine,
        "dns": DnsEngine,
        "udp": UDPEngine,
        "icmp": ICMPEngine,
        "arp": ARPEngine,
    }
    engine_cls = proto_map.get(protocol.lower())
    if engine_cls:
        return engine_cls()
    return None
