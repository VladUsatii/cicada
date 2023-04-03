import sys, os, socket, time, struct, threading, hashlib, dbm, json
from utils import public
from constants import *

def pack_verack():
	message = struct.pack("<L", MAINNET)
	message += struct.pack("12s", b"verack\x00\x00\x00\x00")
	checksum = hashlib.sha256(hashlib.sha256(message).digest()).digest()[:4]
	message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))
	return message

def send_verack(verack, addr_from):
	s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	s.connect(addr_from)
	s.sendall(verack)
	s.close()

