from Message import Message

class ElectionMessage(Message):
	def __init__(self, sourceId, destinationId):
		self.sourceId = sourceId
		self.destinationId = destinationId
		self.subject = 'election'

	def getMessage(self):
		return 'Election from ' + str(self.sourceId) 
