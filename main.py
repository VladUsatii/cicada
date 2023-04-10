#!/usr/bin/env python3
import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from verack import pack_verack, send_verack
from networkaddr import unpack_netaddr
from message_struct import *

def main(HOST: str, PORT: int, my_nonce: int):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	while True:
		conn, addr = s.accept()
		with conn:
			print(f"Connection from {addr}")
			data = conn.recv(1024) # increase to 4096 or 8192 in future
			did_verack = False # marks whether or not the users have exchanged versions
			while data:
				try:
					vers = unpack_message(data, my_nonce) # returns (verack, True) if successful
					if vers[1] is True:
						did_verack = vers[1]
						send_verack(vers[0], addr)
				except Exception as e:
					print("Version message rejected.")
					print("Error: ", e)
				data = conn.recv(1024)
			print("Connection closed")

if __name__ == "__main__":
	my_nonce = struct.unpack('Q', os.urandom(8))[0]
	HOST, PORT = ('0.0.0.0', 1513)
	main(HOST, PORT, my_nonce)
