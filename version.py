import sys, os, socket, time
import struct
import dbm
import json
import threading
import hashlib

from utils import public

version = 0xAB44AB55
command = b"version\x00\x00\x00\x00"
payload = b""
payload_length = len(payload)
checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

# Pack the fields into a binary message
message = struct.pack("<L", version)  # magic field in little endian
message += struct.pack("12s", command)  # command field as a string of 12 bytes
message += struct.pack("<L", payload_length)  # payload length in little endian
message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))  # checksum in little endian
message += payload

print(message)
print(len(message))
