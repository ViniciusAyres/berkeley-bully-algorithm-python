from Message import Message

class ElectionResponseMessage(Message):
	def __init__(self, sourceId, destinationId):
		self.sourceId = sourceId
		self.destinationId = destinationId
		self.subject = 'election_response'

	def getMessage(self):
		return ' Election response  from ' + str(self.sourceId) 
