import socket
import json
import dbm.ndbm

"""
JSON-RPC2 Headers Service

Function checks method of incoming JSON:
- set (writes to headers db)
- get (returns full block from headers db)
- serve_forever (serves on localhost:8086 until stopped)
- handle_request (tries to work with input method, else returns error)

"""
class HeadersService:
	def __init__(self, host='', port=8086):
		self.db = dbm.ndbm.open('headers', 'c')
		self.host, self.port = host, port

	def set(self, key, value):
		self.db[key.encode()] = json.dumps(value).encode()

	def get(self, key):
		value = self.db.get(key.encode())
		if value is None: return None
		return json.loads(value.decode())

	def serve_forever(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.bind((self.host, self.port))
			sock.listen(1)
			print(f'Serving on {self.host}:{self.port}...')
			while True:
				conn, addr = sock.accept()
				with conn:
					print(f'Connected by {addr}')
					data = b''
					while True:
						chunk = conn.recv(1024)
						if not chunk: break
						data += chunk
						try:
							print("Received data.")
							request = json.loads(data.decode())
							response = self.handle_request(request)
							conn.sendall(json.dumps(response).encode())
							break
						except json.JSONDecodeError:
							pass

	def handle_request(self, request):
		try:
			method = getattr(self, request['method'])
			result = method(*request['params'])
			return {
				'jsonrpc': '2.0',
				'result': result,
				'id': request.get('id')
			}
		except Exception as e:
			return {
				'jsonrpc': '2.0',
				'error': {
					'code': 0,
					'message': str(e)
				},
				'id': request.get('id')
			}

if __name__ == '__main__':
	cache = HeadersService()
	cache.serve_forever()
