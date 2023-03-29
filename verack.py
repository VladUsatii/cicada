import sys, os, socket, time
import struct
import dbm
import json
import threading
import hashlib

from utils import public

version = 0xAB44AB55
command = b"verack\x00\x00\x00\x00"

version_enc = struct.pack("<L", version)
command_enc = struct.pack("12s", command)
checksum = hashlib.sha256(hashlib.sha256(version_enc + command_enc).digest()).digest()[:4]

message = version_enc  # magic field in little endian
message += command_enc  # command field as a string of 12 bytes
message += struct.pack("<L", int.from_bytes(checksum, byteorder="little"))  # checksum in little endian

print(message)
print(len(message))
