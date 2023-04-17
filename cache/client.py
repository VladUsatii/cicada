import socket, json

HOST, PORT = 'localhost', 8086

def send_request(method, params=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        request = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': '{}'
        }
        sock.sendall(json.dumps(request).encode())
        print("Sent request.")
        data = sock.recv(1024)
        print("Received response.")
        response = json.loads(data.decode())
        print(response)
        if 'error' in response:
            raise Exception(response['error']['message'])
        return response['result']

#if __name__ == '__main__':
#    value = send_request('set', ['header_here'])
#    print(value)
