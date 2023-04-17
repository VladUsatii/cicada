import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from networkaddr import get_ipv6_address, gen_network_addr, unpack_netaddr
import constants

class Block(object):
	def __init__(self, version: int, prev_block: str, merkle_root: str, timestamp: int, bits: int, nonce: int, txn_count: bytes = None, txns: list = None):
		self.version = struct.pack("<L", version)
		self.prev_block = struct.pack("32s", prev_block)
		self.merkle_root = struct.pack("32s", merkle_root)
		self.timestamp = struct.pack("<q", timestamp)
		self.bits = struct.pack("<q", bits)
		self.nonce = struct.pack("<q", nonce)
		self.txn_count = txn_count
		self.txns = txns

	def add_packed_tx(self, tx: bytes):
		self.txns = self.txns + tx
		self.txn_count += 1

	def pack_block(self):
		return self.version + self.prev_block + self.merkle_root + self.timestamp + self.bits + self.nonce + self.txn_count + self.txns

def unpack_block(message: bytes) -> dict:
	raw = {}
	raw['version'] = struct.unpack("<L", message[:4])[0]
	raw['prev_block'] = struct.unpack("32s", message[4:36])[0]
	raw['merkle_root'] = struct.unpack("32s", message[36:68])[0]
	raw['timestamp'] = struct.unpack("<q", message[68:72])[0]
	raw['bits'] = struct.unpack("<q", message[72:76])[0]
	raw['nonce'] = struct.unpack("<q", message[76:80])[0]
	raw['txn_count'], n = decode_vli(message[80:], True)
	raw['tx'] = message[80+n:]
	return raw


