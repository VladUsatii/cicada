import sys, os, socket, time, struct, dbm, json, threading, hashlib, ipaddress
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from utils import public
import constants as co
from constants import *
from version import *
from message_struct import *
from networkaddr import get_local_ipv4

# testing the packing and unpacking of version message

NONCE = struct.unpack('Q', os.urandom(8))[0]
vers = pack_version(0xafafafaf, co.NODE_NETWORK | co.NODE_BLOOM, int(time.time()), NONCE)
msg = pack_message(0xafafafaf, b"version\x00\x00\x00\x00\x00", vers)

ipv4_address = "192.168.0.11" # address of the fullnode (NOTE: This address is a test)

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.connect((ipv4_address, 1513)) # connect to destination node's address and port
s.sendall(msg) # send data to the node
resp = s.recv(1024)
print(resp)
s.close()

#s.bind((get_local_ipv4(), 1513)) # may work later

