import struct, socket, ipaddress, requests

def get_ipv6_address() -> bytes:
	ipv4_addr = requests.get('https://ipinfo.io/ip').text.strip()
	ipv6_addr = ipaddress.IPv6Address("::ffff:" + ipv4_addr)
	return ipv6_addr.packed

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
