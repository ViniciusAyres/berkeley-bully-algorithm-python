from Message import Message

class NewElectionMessage(Message):
	def __init__(self, sourceId, destinationId):
		self.sourceId = sourceId
		self.destinationId = destinationId
		self.subject = 'new_election'

	def getMessage(self):
		return ' New election from ' + str(self.sourceId) 
