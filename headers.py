import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from networkaddr import get_ipv6_address, gen_network_addr, unpack_netaddr
import constants

def encode_vli(x: int) -> bytes:
	if x < 0: raise ValueError("Value must be non-negative")
	if x == 0: return b'\x00'
	result = bytearray()
	while x:
		# Take the least significant 7 bits of the value and set the most significant bit to 1
		byte = x & 0x7f | 0x80
		result.append(byte)
		x >>= 7
	# Set the most significant bit of the last byte to 0
	result[-1] &= 0x7f
	return bytes(result)

def decode_vli(data: bytes) -> int:
	result = 0
	shift = 0
	for byte in data:
		result |= (byte & 0x7f) << shift
		shift += 7
		if not byte & 0x80: break
	return result

# block headers response (in response to getheaders)
def pack_headers(version: int, prev_block: bytes, merkle_root: bytes, timestamp: int, bits: int, nonce: int, tx_count: int = 0) -> bytes:
	tx_count = encode_vli(tx_count)
	message = struct.pack("<L", version)
	message += struct.pack("32s", prev_block) # 32-byte hash digest
	message += struct.pack("32s", merkle_root) # 32-byte hash digest of full block's tx-list
	message += struct.pack("<q", timestamp) # timestamp of block's creation date
	message += struct.pack("<q", bits) # difficulty of block
	message += struct.pack("<q", nonce) # nonce used to generate the block
	message += tx_count
	return message

def unpack_headers(payload: bytes) -> dict:
	raw = {}
	raw['version'] = struct.unpack("<L", payload[:4])[0]
	raw['prev_block'] = struct.unpack("32s", payload[4:36])[0]
	raw['merkle_root'] = struct.unpack("32s", payload[36:68])[0]
	raw['timestamp'] = struct.unpack("<q", payload[68:72])[0]
	raw['bits'] = struct.unpack("<q", payload[72:76])[0]
	raw['nonce'] = struct.unpack("<q", payload[76:80])[0]
	raw['tx_count'] = decode_vli(payload[80:])
	return raw
