import asyncio
import time
import dns.asyncquery
import dns.message
from sasta_dpi.core.engine import BaseEngine, Response
from sasta_dpi.core.session import PacketConfig

class DnsEngine(BaseEngine):
    async def send(self, config: PacketConfig) -> Response:
        target = config.target
        # DNS usually targets a DNS server, target could be the nameserver to query
        # But if user types a domain to resolve, the `target` might be the domain 
        # and we need an option for the nameserver. Let's assume target is the NS 
        # and option `query` is the domain for this example
        port = config.port if config.port else 53
        
        qname = config.options.get("query", "example.com")
        rtype = config.options.get("record_type", "A")
        
        start_time = time.time()
        try:
            q = dns.message.make_query(qname, rtype)
            # using target as nameserver IP
            resp = await dns.asyncquery.udp(q, target, port=port, timeout=5.0)
            
            latency = (time.time() - start_time) * 1000
            
            answers = []
            for rrset in resp.answer:
                answers.append(rrset.to_text())
                
            summary = f"Answers: {len(resp.answer)}" if resp.answer else "NXDOMAIN or No Answer"
            
            return Response(
                raw_data=resp.to_wire(),
                summary=summary,
                status="Success" if resp.answer else "Warning",
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
        qname = config.options.get("query", "example.com")
        rtype = config.options.get("record_type", "A")
        q = dns.message.make_query(qname, rtype)
        return str(q)
