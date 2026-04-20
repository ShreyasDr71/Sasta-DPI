import time
import asyncio
from sasta_dpi.core.engine import BaseEngine, Response
from sasta_dpi.core.session import PacketConfig
from sasta_dpi.core.capabilities import is_admin

class ARPEngine(BaseEngine):
    async def send(self, config: PacketConfig) -> Response:
        if not is_admin():
            return Response(
                raw_data=b"",
                summary="Admin/root privileges required for raw ARP sockets",
                status="Error",
                latency=0
            )
            
        import scapy.all as scapy
        
        target = config.target
        timeout = float(config.options.get("timeout", 2.0))
        
        start_time = time.time()
        
        loop = asyncio.get_running_loop()
        
        def _send_arp():
            packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=target)
            return scapy.srp1(packet, timeout=timeout, verbose=0)
            
        try:
            # We use srp1 for layer 2
            resp_packet = await loop.run_in_executor(None, _send_arp)
            latency = (time.time() - start_time) * 1000
            
            if resp_packet:
                return Response(
                    raw_data=bytes(resp_packet),
                    summary=f"MAC: {resp_packet[scapy.ARP].hwsrc}",
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
        return f"Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst='{config.target}')"
