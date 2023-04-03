import sys, os, socket, time, struct, dbm, json, threading, hashlib

from utils import public
from networkaddr import get_ipv6_address, gen_network_addr

from constants import *

try:
	DESTINATION_NODE_IPV6 = get_ipv6_address() # dummy address is self for now
except:
	DESTINATION_NODE_IPV6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334" # dummy address when catched

command = b"version\x00\x00\x00\x00"
services = NODE_NETWORK | NODE_BLOOM
timestamp = int(time.time())
payload_length = 0
nonce_bytes = os.urandom(8)
nonce = struct.unpack('Q', nonce_bytes)[0]

message = struct.pack("<L", MAINNET)  # magic field in little endian
message += struct.pack("<Q", services) # services field is a bitmap of 8 bytes
message += struct.pack("<q", timestamp)
message += gen_network_addr(timestamp, services, DESTINATION_NODE_IPV6, 1513, True)
message += struct.pack("12s", command)  # command field as a string of 12 bytes
message += struct.pack("<L", payload_length)  # payload length in little endian
message += struct.pack("Q", nonce)
checksum = hashlib.sha256(hashlib.sha256(message).digest()).digest()[:4]
message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))  # checksum in little endian

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
peer_ip = "2001:db8::1"
peer_port = 1513
s.connect((peer_ip, peer_port))
s.sendall(message)

resp = s.recv(20)
response_magic, response_command, response_length, response_checksum = struct.unpack("<L12sL4s", response_header)
print(resp)
s.close()
