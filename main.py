#!/usr/bin/env python3
import sys, os, socket, time, struct, dbm, json, threading, hashlib

from utils import public
from verack import pack_verack, send_verack
from networkaddr import unpack_netaddr

"""
Reads version of protocol and establishes connection if protocols are matching
"""
def handle_version_message(message: bytes):
	fields = {}
	fields['magic'] = struct.unpack("<L", message[:4])[0]
	fields['services'] = struct.unpack("<Q", message[4:12])[0]
	fields['timestamp'] = struct.unpack("<q", message[12:20])[0]
	fields['address'] = message[20:46]
	fields['command'] = message[46:58].rstrip(b"\x00").decode("ascii")
	fields['payload_length'] = struct.unpack("<L", message[58:62])[0]
	fields['nonce'] = struct.unpack("Q", message[62:70])[0]
	fields['checksum'] = message[70:74]

	calculated_checksum = hashlib.sha256(hashlib.sha256(message[:70]).digest()).digest()[:4]
	if calculated_checksum != fields['checksum']:
		print("Invalid checksum!")
		return

	print(f"Magic: 0x{magic:X}")
	print(f"Command: {command.decode('ascii')}")
	print(f"Payload Length: {payload_length}")
	print(f"Payload: {payload.decode('ascii')}")
	print("Sending verack...")

	addr_from = unpack_netaddr(address, True)
	verack = pack_verack()
	send_verack(verack, addr_from["ipv6"])

"""
Cicada client accepts packed messages and interprets them
"""
def main(HOST: str, PORT: int):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	while True:
		conn, addr = s.accept()
		with conn:
			print(f"Connection from {addr}")
			data = conn.recv(1024)
			while data:
				try:
					handle_version_message(data)
				except Exception as e:
					print("Version message rejected.")
					print("Error: ", e)
				data = conn.recv(1024)
			print("Connection closed")

if __name__ == "__main__":
	HOST, PORT = ('0.0.0.0', 1513)
	main(HOST, PORT)
