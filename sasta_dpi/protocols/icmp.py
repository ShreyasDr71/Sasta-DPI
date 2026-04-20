import time
import asyncio
from sasta_dpi.core.engine import BaseEngine, Response
from sasta_dpi.core.session import PacketConfig
from sasta_dpi.core.capabilities import is_admin

class ICMPEngine(BaseEngine):
    async def send(self, config: PacketConfig) -> Response:
        if not is_admin():
            return Response(
                raw_data=b"",
                summary="Admin/root privileges required for raw ICMP sockets",
                status="Error",
                latency=0
            )
            
        import scapy.all as scapy
        
        target = config.target
        timeout = float(config.options.get("timeout", 2.0))
        
        start_time = time.time()
        
        # Run scapy blocking call in executor
        loop = asyncio.get_running_loop()
        
        def _send_icmp():
            packet = scapy.IP(dst=target)/scapy.ICMP()
            return scapy.sr1(packet, timeout=timeout, verbose=0)
            
        try:
            resp_packet = await loop.run_in_executor(None, _send_icmp)
            latency = (time.time() - start_time) * 1000
            
            if resp_packet:
                return Response(
                    raw_data=bytes(resp_packet),
                    summary=f"Reply from {resp_packet[scapy.IP].src}",
                    status="Success",
                    latency=latency
                )
            else:
                return Response(
                    raw_data=b"",
                    summary="Request timed out",
                    status="Timeout",
                    latency=latency
                )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return Response(
                raw_data=str(e).encode(),
                summary=str(e),
                status="Error",
                latency=latency
            )

    def build_packet(self, config: PacketConfig):
        # returns representation of the packet
        return f"IP(dst={config.target})/ICMP()"
