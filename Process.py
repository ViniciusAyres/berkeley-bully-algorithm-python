import pickle
import threading
from socket import *
from random import randint
from Timer import Timer
from PingMessage import PingMessage
from NewElectionMessage import NewElectionMessage
from ElectionResponseMessage import ElectionResponseMessage

class Process:
	DEFAULT_PORT = 37022

	def __init__(self):
		self.pid = randint(0,1000)
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
		client.bind(("", self.DEFAULT_PORT))

		while(True):
			data, addr = client.recvfrom(1024)
			message = pickle.loads(data)
			if(message.sourceId != self.pid):
				print('received message: %s' %message)				
				if (message.subject == "ping"):
					print(message.getMessage())
				elif (message.subject == "new_election"):
					if (self.pid > message.sourceId):
						self.__electionResponse(addr)
				elif (message.subject == "election_response"):
					print(message.getMessage())
						


	
	def __sendBroadcastMessage(self, message):
		data = pickle.dumps(message)
		self.broadcastSocket.sendto(data, ('<broadcast>', self.DEFAULT_PORT))

	def __sendMessage(self, message, address,  port):
		data = pickle.dumps(message)
		self.udpSocket.sendto(data, (address, port))

	def __initSockets(self):
		self.udpSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		self.broadcastSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		self.broadcastSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		
	def __randomPing(self, interval):
		message = PingMessage(self.pid, 0)
		self.__sendBroadcastMessage(message)
		threading.Timer(interval, self.__randomPing, args=[interval]).start()

	def __newElection(self):
		message = NewElectionMessage(self.pid, 0)
		self.__sendBroadcastMessage(message)

	def __electionResponse(self, adress):
		message = ElectionResponseMessage(self.pid, 0)
		self.__sendMessage(message, adress)

