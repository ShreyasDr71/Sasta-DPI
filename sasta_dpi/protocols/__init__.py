from .tcp import TCPEngine
from .http import HttpEngine
from .dns import DnsEngine

def get_engine(protocol: str):
    proto_map = {
        "tcp": TCPEngine,
        "http": HttpEngine,
        "dns": DnsEngine,
    }
    engine_cls = proto_map.get(protocol.lower())
    if engine_cls:
        return engine_cls()
    return None
