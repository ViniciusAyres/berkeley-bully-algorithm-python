from Message import Message

class CoordinatorPingMessage(Message):
	def __init__(self, sourceId, destinationId):
		self.sourceId = sourceId
		self.destinationId = destinationId
		self.subject = 'coordinator ping'

	def getMessage(self):
		return 'Ping from ' + str(self.sourceId) 
