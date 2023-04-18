#!/usr/bin/env python3
import sys, os, socket, time, struct, dbm, json, threading, hashlib, signal
from utils import public
from verack import pack_verack, send_verack
from networkaddr import unpack_netaddr
from message_struct import *

def handle_connection(conn, addr, my_nonce, s):
	print(f"Connection from {addr}")
	data = conn.recv(1024) # increase to 4096 or 8192 in future
	did_verack = False # marks whether or not the users have exchanged versions
	while data:
		try:
			if did_verack is False:
				vers = unpack_message(data, my_nonce) # returns (verack, True) if successful
				if vers[1] is True:
					did_verack = vers[1]
					send_verack(vers[0], addr, s)
			else:
				msg = unpack_message(data, my_nonce) # returns msg that is ready to send
				conn.sendall(msg) # Send the msg variable back to the other user
		except Exception as e:
			print("Error: ", e)
		data = conn.recv(1024)
	print(f"Connection from {addr} closed")

def main(HOST: str, PORT: int, my_nonce: int, max_connections: int):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(max_connections)
	threads = []
	while True:
		print(f"Accepting on thread {len(threads)}.")
		conn, addr = s.accept()
		if len(threads) >= max_connections:
			print(f"Maximum number of connections reached ({max_connections}), rejecting connection from {addr}.")
			conn.close()
		else:
			t = threading.Thread(target=handle_connection, args=(conn, addr, my_nonce, s))
			t.start()
			threads.append(t)

if __name__ == "__main__":
	try:
		my_nonce = struct.unpack('Q', os.urandom(8))[0]
		HOST, PORT = ('0.0.0.0', 1513)
		max_connections = 5 # Change this to the desired maximum number of connections
		main(HOST, PORT, my_nonce, max_connections)
	except KeyboardInterrupt:
		print("\n[PANIC] Interruption given.")

"""
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
					if did_verack is False:
						vers = unpack_message(data, my_nonce) # returns (verack, True) if successful
						if vers[1] is True:
							did_verack = vers[1]
							send_verack(vers[0], addr, s)
					else:
						msg = unpack_message(data, my_nonce) # returns msg that is ready to send
						conn.sendall(msg)
				except Exception as e:
					print("Error: ", e)
				data = conn.recv(1024)
			print("Connection closed")

if __name__ == "__main__":
	my_nonce = struct.unpack('Q', os.urandom(8))[0]
	HOST, PORT = ('0.0.0.0', 1513)
	main(HOST, PORT, my_nonce)
"""
