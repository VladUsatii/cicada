import struct
import socket

def get_ipv6_address() -> str:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
        sock.connect(('ipv6.google.com', 80))
        ipv6_address = sock.getsockname()[0]
    finally:
        sock.close()
    return ipv6_address

def gen_network_addr(timestamp: int, services: int, ipv6: str, port: int, is_version: bool) -> bytes:
	if is_version == True:
		networkaddr = struct.pack("")
	else:
		networkaddr = struct.pack("<q", timestamp)
	networkaddr += struct.pack("<Q", services)
	networkaddr += struct.pack("12s", ipv6.encode('utf-8'))
	networkaddr += struct.pack("h", port)
	return networkaddr
