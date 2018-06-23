class Process:
	def __init__(self, pid):
		self.pid = pid

		raw_input("Press Enter to continue...")

	def __str__(self):
		return 'pid: ' + str(self.pid)

	def __listenMessages(self):
		pass
	
	def __sendMessage(self, message):
		pass