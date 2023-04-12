import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from networkaddr import get_ipv6_address, gen_network_addr, unpack_netaddr
import constants

def pack_version(version: int, services: int, timestamp: int, nonce: int, addr=None):
	if addr == None:
		addr = gen_network_addr(timestamp, services, get_ipv6_address(), 1513, True)
	message = struct.pack("<L", version)  # version field in little endian
	message += struct.pack("<Q", services) # services field is a bitmap of 8 bytes
	message += struct.pack("<q", timestamp)
	message += addr
	# TODO: message += addr_from
	message += struct.pack("Q", nonce)
	# TODO: message += user_agent
	# TODO: message += start_height
	# TODO: message += relay
	return message

def unpack_version(payload: bytes) -> dict:
	raw = {}
	raw['version'] = struct.unpack("<L", payload[:4])[0]
	raw['services'] = struct.unpack("<Q", payload[4:12])[0]
	raw['timestamp'] = struct.unpack("<q", payload[12:20])[0]
	raw['addr'] = unpack_netaddr(payload[20:-8], True)
	# TODO: message unpack addr_from
	raw['nonce'] = struct.unpack("Q", payload[-8:])[0]
	# TODO: message unpack user_agent
	# TODO: message unpack start_height
	# TODO: message unpack relay
	return raw

def version_check(message: dict, my_nonce: int) -> bool:
	assert message['version'] >= int(constants.version[::-1], 16), "Versions don't match."
	n_b_s, n_a_s = int(message['services']), int(constants.services)
	assert n_b_s & n_a_s & constants.NODE_NETWORK, "both nodes must support full block requests."
	# TODO: add dynamic permissions
	assert int(message['timestamp']) <= int(time.time()), "Timestamps are forged."
	assert int(my_nonce) != int(message['nonce']), "Nonces match. Nodes can't connect to themselves."
	return True
