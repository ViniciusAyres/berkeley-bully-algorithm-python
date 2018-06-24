from Message import Message

class PingMessage(Message):
	def __init__(self, sourceId, destinationId):
		self.sourceId = sourceId
		self.destinationId = destinationId
		self.subject = 'ping'

	def getMessage(self):
		return 'Ping from ' + str(self.sourceId) 
