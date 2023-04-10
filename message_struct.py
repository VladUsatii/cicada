import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from constants import *
from version import *

# _t means "type" in C format
# < means little-endian
# Capital letters mean Unsigned (non-negative, where MSB is part of value, rather than the sign)
# lowercase letters mean signed (+ or - whole number, where MSB represents negativity rather than value)
# EXAMPLES:
# L means Long, or 4-byte unsigned integer (uint_32)
# l means long, or 4-byte signed integer (int_32)
# Q means Quad, or 8-byte unsigned integer (uint_64)
# q means quad, or 8-byte signed integer (int_64)
# 12s means 12-byte string (char[12])

def pack_message(magic: int, command: bytes, payload: bytes) -> bytes:
	assert isinstance(payload, bytes), "Payload must already be packed"
	checksum = struct.unpack("<L", public.dhash(payload)[:4])[0]
	length = len(payload)
	message = struct.pack("<L", magic)
	message += struct.pack("12s", command)
	message += struct.pack("<L", length)
	message += struct.pack("<L", checksum)
	message += payload
	return message

def unpack_message(message: bytes, my_nonce: int) -> dict:
	payload = message[24:]

	raw = {}
	raw['magic'] = struct.unpack("<L", message[:4])[0]
	raw['command'] = struct.unpack("12s", message[4:16])[0]
	raw['length'] = struct.unpack("<L", message[16:20])[0]
	raw['checksum'] = struct.unpack("<L", message[20:24])[0]
	raw['payload'] = payload

	if raw['checksum'] != struct.unpack("<L", public.dhash(payload)[:4])[0]:
		return None
	if raw['length'] != len(payload):
		return None

	if raw['command'] == b"version\x00\x00\x00\x00\x00":
		message = unpack_version(payload)
		print("received message: ", message)
		if version_check(message, my_nonce):
			verack = pack_verack()
			return (verack, True)
	elif raw['command'] == b"verack\x00\x00\x00\x00\x00\x00":
		pass
	elif raw['command'] == b"getblocks\x00\x00\x00":
		pass
	elif raw['command'] == b"getheaders\x00\x00":
		pass
	elif raw['command'] == b"getdata\x00\x00\x00\x00\x00":
		pass
	elif raw['command'] == b"ping\x00\x00\x00\x00\x00\x00\x00\x00":
		pass
	elif raw['command'] == b"addr\x00\x00\x00\x00\x00\x00\x00\x00":
		pass
	elif raw['command'] == b"tx\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
		pass
	else:
		print("No command found.")
		pass
