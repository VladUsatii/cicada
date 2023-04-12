import sys, os, socket, time, struct, threading, hashlib, dbm, json
from utils import public
import constants

"""
verack is the only message that doesn't follow the standard
payload packing procedure. It is sent in as simple of a
format as possible.
"""
def pack_verack() -> bytes:
	message = struct.pack("<L", constants.MAINNET)
	message += struct.pack("12s", b"verack\x00\x00\x00\x00")
	message += struct.pack('4B', 0, 0, 0, 0) # empty payload
	checksum = hashlib.sha256(hashlib.sha256(message).digest()).digest()[:4]
	message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))
	return message

# sends to the IPv4-mapped IPv6 address of the emitting node
def send_verack(verack, addr_from: tuple):
	ipv4_address = addr_from[0]
	#ipv6_address = socket.inet_ntop(socket.AF_INET6, socket.inet_pton(socket.AF_INET6, f"::ffff:{ipv4_address}"))
	print("Sending verack to: ", ipv4_address)
	s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	s.connect((ipv4_address, addr_from[1]))
	s.sendall(verack)
	s.close()

