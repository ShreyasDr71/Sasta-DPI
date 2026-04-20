from textual.app import ComposeResult
from textual.widgets import Static, Select, Input, Label
from textual.containers import Vertical

class ConfigPane(Static):
    PROTOCOLS = [
        ("TCP", "tcp"),
        ("UDP", "udp"),
        ("ICMP", "icmp"),
        ("HTTP", "http"),
        ("DNS", "dns"),
        ("NTP", "ntp"),
        ("SNMP", "snmp"),
        ("SSDP", "ssdp"),
        ("SMB", "smb"),
        ("LDAP", "ldap"),
        ("NetBIOS", "netbios"),
        ("DHCP", "dhcp"),
        ("Kerberos", "kerberos"),
        ("ARP", "arp")
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Protocol Config"),
            Select(self.PROTOCOLS, prompt="Select protocol", id="protocol-select", value="tcp"),
            Label("Target Host"),
            Input(placeholder="e.g., 192.168.1.1 or example.com", id="target-input"),
            Label("Target Port"),
            Input(placeholder="e.g., 80", id="port-input"),
            id="config-container"
        )
