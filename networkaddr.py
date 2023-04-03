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

def unpack_netaddr(address: bytes, is_version: bool) -> dict:
	fields = {}
	n = 0
	if is_version == True: n = 4

	fields["timestamp"] = struct.unpack("q", address[:8 - n])[0]
	fields["services"] = struct.unpack("<Q", address[8 - n:16 - n])[0]
	fields["ipv6"] = struct.unpack("12s", address[16 - n:-4][0]
	fields["port"] = struct.unpack("h", address[-4:])[0]
	return fields
