import sys, os, socket, time, struct, threading, hashlib, dbm, json
from utils import public
import constants

def pack_verack() -> bytes:
	message = struct.pack("<L", constants.MAINNET)
	message += struct.pack("12s", b"verack\x00\x00\x00\x00")
	message += struct.pack('4B', 0, 0, 0, 0) # empty payload
	checksum = hashlib.sha256(hashlib.sha256(message).digest()).digest()[:4]
	message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))
	return message
