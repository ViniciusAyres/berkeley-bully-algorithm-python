from Message import Message

class SynchronizeTimeResponseMessage(Message):
  def __init__(self, sourceId, destinationId, time):
    self.sourceId = sourceId
    self.destinationId = destinationId
    self.time = time
    self.subject = 'synchronization response'
    
  def getMessage(self):
    return self.time
