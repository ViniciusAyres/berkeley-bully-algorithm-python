import socket
import pickle
import threading

class Process:
	PORT = 37022

	def __init__(self, pid):
		self.pid = pid

		listener = threading.Thread(target=self.__listenMessages)
		raw_input('Press Enter to continue...')
		listener.start()

	def __str__(self):
		return 'pid: ' + str(self.pid)

	def __listenMessages(self):
		print('Waiting messages...')
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		client.bind(("", self.PORT))

		while(True):
			data, addr = client.recvfrom(1024)
			message = pickle.loads(data)
			print('received message: %s' %message)
	
	def __sendMessage(self, message):
		pass