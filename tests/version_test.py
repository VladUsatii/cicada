import sys, os, socket, time, struct, dbm, json, threading, hashlib, ipaddress
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from utils import public
from constants import *
from version import *
from message_struct import *

# testing the packing and unpacking of version message

NONCE = struct.unpack('Q', os.urandom(8))[0]
version = pack_version(0xafafafaf, NODE_NETWORK | NODE_BLOOM, int(time.time()), NONCE)
msg = pack_message(0xafafafaf, b"version\x00\x00\x00\x00\x00", version)

ipv4_address = "192.0.2.235" # TODO: Replace with destination node's IPv4 public address
ipv6_address = ipaddress.IPv6Address("::ffff:" + ipv4_address).packed

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.connect((ipv6_address, 1513)) # connect to destination node's address and port
s.sendall(msg) # send data to the node
s.close()
