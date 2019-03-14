# создание сокета, клиент
import socket
import time

class ClientError(Exception):
	"""Класс для генерации ошибок работы протокола"""
	pass

class Client:
	def __init__(self, host, port, timeout = None):
		self.host = host
		self.port = port
		self.timeout = timeout
		try:
			self.conn = socket.create_connection((host, port), timeout)
		except socket.error as err:
			raise ClientError("error create connection", err)

	def _read(self):
		data = b''
		while not data.endswith(b"\n\n"):
			try:
				data += self.conn.recv(1024)
			except socket.error as err:
				raise ClientError("error recv data", err)

		decoded_data = data.decode()
		return decoded_data.strip()
		#status, payload = decoded_data.split("\n", 1)
		#payload = payload.strip()
		#print(payload)
		#if status == "error":
		#	raise ClientError(payload)
        
		#return payload

	def put(self, metric, value, timestamp = str(int(time.time()))):
		try:
			self.conn.sendall('put {} {} {}\n'.format(metric, value,
											timestamp).encode("utf8"))
		except socket.error as err:
			raise ClientError("error send data", err)

		return self._read()

	def get(self, metric):
		try:
			self.conn.sendall('get {}\n'.format(metric).encode("utf8"))
		except socket.error as err:
			raise ClientError("error send data", err)

		return self._read()
		
		#payload = self._read()
		
		#data = {}
		#if payload == "":
		#	return data
 
		#for row in payload.split("\n"):
		#	key, value, timestamp = row.split()
		#	if key not in data:
		#		data[key] = []
		#	data[key].append((int(timestamp), float(value)))
 
		#return data
		
	def close(self):
		try:
			self.conn.close()
		except socket.error as err:
			raise ClientError("error close connection", err)

client = Client('127.0.0.1', 10000, timeout = 20)
print(client.put("palm.cpu", 0.5, timestamp = 1150864247))
print(client.put("palm.cpu", 2.0, timestamp=1150864248))
time.sleep(1)
client.put("eardrum.cpu", 3, timestamp=1150864250)
time.sleep(1)
client.put("eardrum.cpu", 4, timestamp = 1150864251)
time.sleep(1)
client.put("eardrum.memory", 4200000)
time.sleep(1)
print(client.get("palm.cpu"))
time.sleep(1)
print(client.get("*"))


