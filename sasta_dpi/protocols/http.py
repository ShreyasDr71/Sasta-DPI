import asyncio
import time
import httpx
from sasta_dpi.core.engine import BaseEngine, Response
from sasta_dpi.core.session import PacketConfig

class HttpEngine(BaseEngine):
    async def send(self, config: PacketConfig) -> Response:
        target = config.target
        port = config.port
        method = config.options.get("method", "GET")
        path = config.options.get("path", "/")
        
        scheme = "https" if port == 443 else "http"
        url = f"{scheme}://{target}:{port}{path}"
        
        start_time = time.time()
        try:
            async with httpx.AsyncClient(verify=False, timeout=5.0) as client:
                req = client.build_request(method, url)
                resp = await client.send(req)
            
            latency = (time.time() - start_time) * 1000
            status = "Success" if resp.status_code < 400 else "Warning"
            
            # Simple hex dump representation of the HTTP response for capture pane
            raw_data = f"HTTP/{resp.http_version} {resp.status_code} {resp.reason_phrase}\r\n".encode()
            for k, v in resp.headers.items():
                raw_data += f"{k}: {v}\r\n".encode()
            raw_data += b"\r\n" + resp.content
            
            return Response(
                raw_data=raw_data,
                summary=f"HTTP {resp.status_code} {len(resp.content)} bytes",
                status=status,
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
        # We don't construct a raw scapy HTTP packet usually, httpx does it.
        # This can just return the URL or raw text.
        return f'{config.options.get("method", "GET")} {config.options.get("path", "/")} HTTP/1.1'
