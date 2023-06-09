import urllib.request
import hashlib
import re

def get_public_ip():
	url = "https://checkip.amazonaws.com"
	request = urllib.request.urlopen(url).read().decode("utf-8")
	ip_address = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", request).group(0)
	return ip_address

def dhash(x: bytes):
	return hashlib.sha256(hashlib.sha256(x).digest()).digest()
