class DatabaseError(Excetion):
  ''' Base class for DB errors '''
  pass

class InvalidCollection(DatabaseError):
  ''' Collection does not exist in DB '''
  def __init__(self, value):
    self.message = value
