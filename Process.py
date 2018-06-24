import pickle
import threading
from socket import *
from random import randint
from Timer import Timer
from PingMessage import PingMessage

class Process:
	PORT = 37022

	def __init__(self, pid):
		self.pid = pid
		self.timer = Timer()
		self.__initSocket()
		
		listener = threading.Thread(target=self.__listenMessages)
		raw_input('Press Enter to continue...')
		listener.start()
		self.__randomPing(randint(1, 5))

	def __str__(self):
		return 'pid: ' + str(self.pid)

	def __listenMessages(self):
		print('Waiting messages...')
		client = socket(AF_INET, SOCK_DGRAM)
		client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		client.bind(("", self.PORT))

		while(True):
			data, addr = client.recvfrom(1024)
			message = pickle.loads(data)
			if(message.sourceId != self.pid):
				print('received message: %s' %message)
				print(message.getMessage())
	
	def __sendMessage(self, message):
		data = pickle.dumps(message)
		self.socket.sendto(data, ('<broadcast>', self.PORT))

	def __initSocket(self):
		self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		
	def __randomPing(self, interval):
		message = PingMessage(self.pid, 0)
		self.__sendMessage(message)
		threading.Timer(0.25, self.__randomPing, args=[interval]).start()