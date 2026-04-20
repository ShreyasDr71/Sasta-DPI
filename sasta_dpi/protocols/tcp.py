import asyncio
import time
from sasta_dpi.core.engine import BaseEngine, Response
from sasta_dpi.core.session import PacketConfig

class TCPEngine(BaseEngine):
    async def send(self, config: PacketConfig) -> Response:
        # For simplicity in this demo, without requiring raw socket admin perms 
        # for a basic run, we'll try an asyncio connection (Connect Scan)
        target = config.target
        port = int(config.port) if config.port else 80
        
        start_time = time.time()
        try:
            # We're doing a full connect scan for now
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target, port), timeout=2.0
            )
            writer.close()
            await writer.wait_closed()
            
            latency = (time.time() - start_time) * 1000
            return Response(
                raw_data=b"TCP Connect OK",
                summary="Port Open",
                status="Open",
                latency=latency
            )
        except (asyncio.TimeoutError, ConnectionRefusedError) as e:
            latency = (time.time() - start_time) * 1000
            return Response(
                raw_data=str(e).encode(),
                summary="Connection Refused / Timeout",
                status="Closed",
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
        return f"TCP connect() to {config.target}:{config.port}"
