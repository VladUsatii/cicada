import sys, os, socket, time
import struct
import dbm
import json
import threading
import hashlib

from utils import public
from networkaddr import get_ipv6_address, gen_network_addr

from constants import *

DESTINATION_NODE_IPV6 = get_ipv6_address() # dummy address is self for now

version = 0xAB44AB55
command = b"version\x00\x00\x00\x00"
services = NODE_NETWORK | NODE_BLOOM
timestamp = int(time.time())
payload = b""
payload_length = len(payload)
nonce_bytes = os.urandom(8)
nonce = struct.unpack('Q', nonce_bytes)[0]
checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

# Pack the fields into a binary message
message = struct.pack("<L", version)  # magic field in little endian
message += struct.pack("<Q", services) # services field is a bitmap of 8 bytes
message += struct.pack("<q", timestamp)
message += gen_network_addr(timestamp, services, DESTINATION_NODE_IPV6, 1513, True)
message += struct.pack("12s", command)  # command field as a string of 12 bytes
message += struct.pack("<L", payload_length)  # payload length in little endian
message += struct.pack("Q", nonce)
message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))  # checksum in little endian
message += payload

print(message)
