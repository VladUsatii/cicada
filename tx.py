import sys, os, socket, time, struct, dbm, json, threading, hashlib
from utils import public
from networkaddr import get_ipv6_address, gen_network_addr, unpack_netaddr
import constants

class Transaction(object):
	def __init__(self):
		self.version = None
		self.flag = None
		self.tx_in_count, self.tx_in = None, None
		self.tx_out_count, self.tx_out = None, None
		self.tx_witnesses = None
		self.lock_time = None
