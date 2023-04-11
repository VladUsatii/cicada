import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from networkaddr import get_ipv6_address, gen_network_addr, unpack_netaddr
import constants

# ping (also used for pong, but command is different)
# confirms UDP conection is still valid

def pack_ping(nonce: int) -> bytes:
	return struct.pack("Q", nonce)

def unpack_ping(payload: bytes) -> dict:
	return {"nonce": struct.unpack("Q", payload)}

# getaddr
# request a list of known nodes' IPv4-mapped IPv6 addresses

def pack_getaddr(count: int) -> bytes:
	return struct.pack("<L", count) # count field in little endian

def unpack_getaddr(payload: bytes) -> dict:
	return {"count": struct.unpack("<L", payload)[0]}

# addr
# sends a list of known nodes' addresses

def pack_addr(count: int) -> bytes:
	pass

def unpack_addr(payload: bytes) -> dict:
	addresses = []
	# TODO: Finish getting a random list of known nodes
	return {"addrs": [x for x in addresses]}


# reject
# error code sent to node if message is incorrectly formulated

def pack_reject() -> bytes:
	#TODO: message, ccode, reason, data
	pass
