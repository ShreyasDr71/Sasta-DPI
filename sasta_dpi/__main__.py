import click
from sasta_dpi.app import SastaDPI

@click.command()
@click.option('--target', '-t', help='Target IP or hostname')
@click.option('--protocol', '-p', type=click.Choice(['tcp', 'udp', 'icmp', 'http', 'dns', 'ntp', 'snmp', 'ssdp', 'smb', 'ldap', 'netbios', 'dhcp', 'kerberos', 'arp'], case_sensitive=False), help='Protocol to use')
@click.option('--port', help='Target port')
def cli(target, protocol, port):
    """Sasta DPI - TUI for network packet crafting and sending."""
    app = SastaDPI()
    app.run()

if __name__ == '__main__':
    cli()
