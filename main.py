#!/usr/bin/env python3
import sys, os, socket, time
import struct
import dbm
import json
import threading
import hashlib

from utils import public


# TODO: Finish this handler
"""
Reads version of protocol and establishes connection if protocols are matching
"""
def handle_version_message(data: bytes):
	magic = struct.unpack("<L", data[:4])[0]
	command = data[4:16].strip(b"\x00")
	payload_length = struct.unpack("<L", data[16:20])[0]
	checksum = struct.unpack("<L", data[20:24])[0].to_bytes(4, byteorder="little")
	payload = data[24:]

	calculated_checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
	if calculated_checksum != checksum:
		print("Invalid checksum!")
		return

	print(f"Magic: 0x{magic:X}")
	print(f"Command: {command.decode('ascii')}")
	print(f"Payload Length: {payload_length}")
	print(f"Payload: {payload.decode('ascii')}")

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
				handle_version_message(data)
				data = conn.recv(1024)
			print("Connection closed")

if __name__ == "__main__":
	HOST, PORT = ('0.0.0.0', 1513)
	main(HOST, PORT)
