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
		self.__initSockets()
		
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
	
	def __sendBroadcastMessage(self, message):
		data = pickle.dumps(message)
		self.broadcastSocket.sendto(data, ('<broadcast>', self.PORT))

	def __sendMessage(self, message, address):
		data = pickle.dumps(message)
		self.udpSocket.sendto(data, (address, self.PORT))

	def __initSockets(self):
		self.udpSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		self.broadcastSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		self.broadcastSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		
	def __randomPing(self, interval):
		message = PingMessage(self.pid, 0)
		self.__sendBroadcastMessage(message)
		threading.Timer(interval, self.__randomPing, args=[interval]).start()