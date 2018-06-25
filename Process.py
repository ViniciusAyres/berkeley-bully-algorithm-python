import pickle
import threading
from socket import *
from random import randint
from Timer import Timer
from PingMessage import PingMessage
from ElectionMessage import ElectionMessage
from ElectionResponseMessage import ElectionResponseMessage
from SynchronizeTimeMessage import SynchronizeTimeMessage
from UpdateTimeMessage import UpdateTimeMessage
from SynchronizeTimeResponseMessage import SynchronizeTimeResponseMessage

class Process:
	DEFAULT_PORT = 37022
	ELECTION_PORT = 37023
	SYNCHRONIZE_TIME_PORT = 37024
	SYNCHRONIZATION_TIME = 4

	def __init__(self):
		self.isCoordinator = False
		self.pid = randint(0,1000)
		self.timer = Timer()
		self.__initSockets()
		
		print('My id is: %s' %str(self.pid))
		listener = threading.Thread(target=self.__listenMessages)
		election = threading.Thread(target=self.__startElection)
		raw_input('Press Enter to continue...')
		listener.start()
		election.start()
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
				self.__handleMessage(message, addr)
			
	def __handleMessage(self, message, addr):
		print('received message: %s' %message.subject)				
		if (message.subject == "ping"):
			print(message.getMessage())
		elif (message.subject == "election"):
			if (self.pid > message.sourceId):
				self.__electionResponse(addr)					
				election = threading.Thread(target=self.__startElection)
				election.start()
		elif (message.subject == "synchronization"):
			self.__SyncTimeRequest(addr)
		elif (message.subject == "time update"):
			print("Timer atualizado para : " + message.getTime())
			self.timer.setTime(message.getMessage())

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

	def __electionResponse(self, adress):
		message = ElectionResponseMessage(self.pid, 0)
		self.__sendMessage(message, adress, self.ELECTION_PORT)
		
	def __startElection(self):
		print('Starting election...')
		electionSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		electionSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		electionSocket.settimeout(0.5)
		electionSocket.bind(("", self.ELECTION_PORT))
		
		messages = []
		message = ElectionMessage(self.pid, 0)
		self.__sendBroadcastMessage(message)

		try:
			while(True):
				data, addr = electionSocket.recvfrom(1024)
				messages.append(pickle.loads(data))
		except timeout:
			print('Received %s election messages responses' %(len(messages)))

		if len(messages) == 0:
			self.isCoordinator = True
			print('I\'m the new coordinator')
			threading.Timer(self.SYNCHRONIZATION_TIME, self.__synchronizeTimer).start()
		else:
			print('I lost the election.')


	def __synchronizeTimer(self, interval=SYNCHRONIZATION_TIME):
		if self.isCoordinator:
			print('Starting time synchronization...')
			timerSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
			timerSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
			timerSocket.settimeout(0.5)
			timerSocket.bind(("", self.SYNCHRONIZE_TIME_PORT))
			
			time_list = [self.timer.getTime()]
			message = SynchronizeTimeMessage(self.pid, 0)
			self.__sendBroadcastMessage(message)

			try:
				while(True):
					data, addr = timerSocket.recvfrom(1024)
					time_list.append(pickle.loads(data).getMessage())
			except timeout:
				print('Received %s time message responses' %( len(time_list) - 1 ))
			
			updatedTime = reduce(lambda x, y: x + y, time_list) / len(time_list)
			message = UpdateTimeMessage(self.pid, 0, updatedTime)
			self.__sendBroadcastMessage(message)
			threading.Timer(self.SYNCHRONIZATION_TIME, self.__synchronizeTimer).start()

	def __SyncTimeRequest(self, addr):
		print("Request Time...")		
		message = SynchronizeTimeResponseMessage(self.pid, 0, self.timer.getTime())
		self.__sendMessage(message, addr[0], self.SYNCHRONIZE_TIME_PORT)