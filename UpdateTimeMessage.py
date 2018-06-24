from Message import Message

class UpdateTimeMessage(Message):
  def __init__(self, sourceId, destinationId, time):
    self.sourceId = sourceId
    self.destinationId = destinationId
    self.time = time
    self.subject = 'time update'
    
  def getMessage(self):
    return self.time
