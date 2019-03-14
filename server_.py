import socket
import time

dict = {}
def run_server(host, port):
	server = Server(host, port)

#Вызов исключений во избежание аварийного завершения работы модуля из-за системных ошибок.
class ServerError(Exception):
	pass

class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.sock.listen(socket.SOMAXCONN)
		self.sock.settimeout(20)
		self._read()

	def _read(self):
		while True:
			#Системный вызов accept по умолчанию заблокируется до тех пор, пока не появится клиентское соединение. 
			try:
				conn, addr = self.sock.accept()
			except socket.timeout:
				print('Close connection by timeout.')
				break
			data = b''
			while not data.endswith(b'\n'):
				try:
					data += conn.recv(1024)
				except socket.error as err:
					raise ClientError("recv error", err)
			
			data = data[:-1].decode('utf8').split(' ')
			if data[0] == 'get':
				try:
					conn.send(self._put(data))
				except socket.error as err:
					raise ClientError("send error", err)
			else:
				if data[0] == 'put':
					try:
						conn.send(self._get(data))
					except socket.error as err:
						ClientError("send error", err) 
				else:
					try:
						conn.send('error\nwrong command\n\n'.encode('utf8'))
					except socket.error as err:
						ClientError("send error", err)

	def _put(self, data):
		if len(data) != 2:
			return 'error\nwrong command\n\n'.encode('utf8')
		else:
			key = data[1]
			str = b'ok\n'
			if key in dict.keys():
				for i in range(len(dict[key])):
					str += '{} {} {}\n'.format(key, dict[key][i][0], dict[key][i][1]).encode('utf8')
				return str + b'\n'
			else:
				return 'ok\n\n'.encode('utf8')
		

	def _get(self, data):
		if len(data) != 4:
			return 'error\nwrong command\n\n'.encode('utf8')
		else:
			key, value, timestamp = data[1:]
			if key in dict.keys():
				dict[key].append((value, timestamp))
			else:
				dict[key] = [(value, timestamp)]
			print(dict)
			return 'ok\n\n'.encode('utf8')


run_server('127.0.0.1', 10000)
	


