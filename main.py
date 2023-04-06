#!/usr/bin/env python3
import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from verack import pack_verack, send_verack
from networkaddr import unpack_netaddr
from message_struct import *

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
					unpack_message()
				except Exception as e:
					print("Version message rejected.")
					print("Error: ", e)
				data = conn.recv(1024)
			print("Connection closed")

if __name__ == "__main__":
	HOST, PORT = ('0.0.0.0', 1513)
	main(HOST, PORT)
