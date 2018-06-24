from Message import Message

class PingMessage(Message):
	def __init__(self, sourceId, destinationId):
		self.sourceId = self.sourceId
		self.destinationId = self.destinationId
		self.subject = 'ping'

	def getMessage(self):
		return 'Ping from ' + str(self.sourceId) 

