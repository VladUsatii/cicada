import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from networkaddr import get_ipv6_address, gen_network_addr, unpack_netaddr
import constants

def outpoint(reference_hash, index) -> bytes:
	message = struct.pack("32s", reference_hash)
	message += struct.pack("<L", index)
	return message

def tx_in(outpoint: bytes, script_length: bytes, custom_script: str, sequence: int) -> bytes:
	message = outpoint
	message += script_length
	message += custom_script # TODO: Take script_length and use it to interpret the struct.pack("THIS PART", custom_script)
	message += struct.pack("<L", sequence)
	return message

def tx_out(tx_value: int, pk_script_length: bytes, pk_script: str) -> bytes:
	message += struct.pack("<q", tx_value)
	message += pk_script_length
	message += pk_script
	return message

class Transaction(object):
	def __init__(self, version: int, flag, tx_in_count, tx_in, tx_out_count, tx_out, tx_witnesses, lock_time):
		self.version = None
		self.flag = None
		self.tx_in_count, self.tx_in = None, None
		self.tx_out_count, self.tx_out = None, None
		self.tx_witnesses = None
		self.lock_time = None

	def pack_tx(self):
		pass
