from abc import ABCMeta, abstractmethod

#Essa classe eh abstrata, eh pra ser usada como modelo
class Message:
	__metaclass__ = ABCMeta
	
	def __init__(self, sourceId, destinationId, subject):
		self.sourceId = sourceId
		self.destinationId = destinationId
		self.subject = subject

	@abstractmethod
	def getMessage(self):
		pass

	