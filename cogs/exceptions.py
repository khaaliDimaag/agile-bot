class DatabaseError(Exception):
  ''' Base class for DB errors '''
  pass

class InvalidCollection(DatabaseError):
  ''' Collection does not exist in DB '''
  def __init__(self, value):
    self.message = value

class InvalidGuildID(DatabaseError):
  ''' Guild not found in DB '''
  def __init__(self, id):
    self.message = 'Guild ID: ' + str(id)