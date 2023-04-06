import sys, os, socket, time, struct, dbm, json, threading, hashlib
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from utils import public
from constants import *
from version import *
from message_struct import *

# testing the packing and unpacking of version message
version = pack_version(0xafafafaf, NODE_NETWORK | NODE_BLOOM, int(time.time()), struct.unpack('Q', os.urandom(8))[0])
msg = pack_message(0xafafafaf, b"version\x00\x00\x00\x00\x00", version)
print(msg)
raw = unpack_message(msg)
print(raw)
