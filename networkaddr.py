import struct, socket, ipaddress, requests

def get_local_ipv4() -> str:
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.connect(('8.8.8.8', 80))
		private_ip = s.getsockname()[0]
	if private_ip.startswith('192.168.'):
		return private_ip
	else:
		raise ValueError("Not a private IP address")

# gets ipv4-mapped ipv6 or generates mapped from existing ipv4
def get_ipv6_address(ipv4_address: str = None) -> bytes:
	if ipv4_address is None:
		ipv4_addr = requests.get('https://ipinfo.io/ip').text.strip()
		ipv6_addr = ipaddress.IPv6Address("::ffff:" + ipv4_addr)
		return ipv6_addr.packed
	else:
		return socket.inet_pton(socket.AF_INET6, "::ffff:" + ipv4_address)

# returns ipv4 address from packed ipv4-mapped ipv6
def unpack_ipv6_address(packed_ipv6: bytes) -> str:
	ipv6_address = ipaddress.IPv6Address(packed_ipv6)
	ipv4_mapped_address = ipv6_address.ipv4_mapped
	return str(ipv4_mapped_address) if ipv4_mapped_address else None

def gen_network_addr(timestamp: int, services: int, ipv6: str, port: int, is_version: bool) -> bytes:
	if is_version == True:
		networkaddr = struct.pack("")
	else:
		networkaddr = struct.pack("<q", timestamp)
	networkaddr += struct.pack("<Q", services)
	networkaddr += struct.pack("16s", get_ipv6_address())
	networkaddr += struct.pack("h", port)
	return networkaddr

def unpack_netaddr(address: bytes, is_version: bool) -> dict:
	fields = {}
	n = 0
	if is_version == True: n = 8
	if is_version == False:
		fields["timestamp"] = struct.unpack("q", temp[:8])[0]
	fields["services"] = struct.unpack("<Q", address[8 - n:16 - n])[0]
	print(len(address[16 - n:-4]))
	fields["ipv6"] = struct.unpack("16s", address[16 - n:-2])[0]
	fields["port"] = struct.unpack("h", address[-2:])[0]
	return fields
