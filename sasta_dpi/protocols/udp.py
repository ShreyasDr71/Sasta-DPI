import time
import asyncio
from sasta_dpi.core.engine import BaseEngine, Response
from sasta_dpi.core.session import PacketConfig
from sasta_dpi.core.capabilities import is_admin

class UDPEngine(BaseEngine):
    async def send(self, config: PacketConfig) -> Response:
        
        target = config.target
        port = int(config.port) if config.port else 53
        timeout = float(config.options.get("timeout", 2.0))
        payload = config.options.get("payload", b"")
        
        start_time = time.time()

        if is_admin():
            import scapy.all as scapy
            loop = asyncio.get_running_loop()
            
            def _send_udp():
                packet = scapy.IP(dst=target)/scapy.UDP(dport=port)/scapy.Raw(load=payload)
                return scapy.sr1(packet, timeout=timeout, verbose=0)
                
            try:
                resp_packet = await loop.run_in_executor(None, _send_udp)
                latency = (time.time() - start_time) * 1000
                
                if resp_packet:
                    if resp_packet.haslayer(scapy.ICMP):
                        icmp_type = resp_packet[scapy.ICMP].type
                        icmp_code = resp_packet[scapy.ICMP].code
                        if icmp_type == 3 and icmp_code == 3:
                            return Response(
                                raw_data=bytes(resp_packet),
                                summary="Port Unreachable (ICMP)",
                                status="Closed",
                                latency=latency
                            )
                    return Response(
                        raw_data=bytes(resp_packet),
                        summary="Response received",
                        status="Open",
                        latency=latency
                    )
                else:
                    return Response(
                        raw_data=b"",
                        summary="No response (Open|Filtered)",
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
        else:
            # Fallback to standard asyncio UDP (Datagram protocol)
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            
            class UDPClientProtocol(asyncio.DatagramProtocol):
                def __init__(self, target, port):
                    self.target = target
                    self.port = port
                    
                def connection_made(self, transport):
                    self.transport = transport
                    transport.sendto(payload if isinstance(payload, bytes) else payload.encode())

                def datagram_received(self, data, addr):
                    if not future.done():
                        future.set_result(data)

                def error_received(self, exc):
                    if not future.done():
                        future.set_exception(exc)
                        
                def connection_lost(self, exc):
                    if not future.done() and exc is not None:
                         future.set_exception(exc)

            transport, protocol = await loop.create_datagram_endpoint(
                lambda: UDPClientProtocol(target, port),
                remote_addr=(target, port)
            )
            
            try:
                data = await asyncio.wait_for(future, timeout=timeout)
                latency = (time.time() - start_time) * 1000
                return Response(
                    raw_data=data,
                    summary=f"Received {len(data)} bytes",
                    status="Open",
                    latency=latency
                )
            except asyncio.TimeoutError:
                latency = (time.time() - start_time) * 1000
                return Response(
                    raw_data=b"",
                    summary="Request timed out",
                    status="Timeout",
                    latency=latency
                )
            finally:
                transport.close()


    def build_packet(self, config: PacketConfig):
        return f"UDP dport={config.port} to {config.target}"
