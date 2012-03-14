class Direction(object):
  def __init__(self, x=None, y=None):
    self.x = x
    self.y = y
  
  def copy(self):
    return Direction(self.x, self.y)
  
  def flip_y(self):
    return Direction(self.x, -self.y)
  
  def flip_x(self):
    return Direction(-self.x, self.y)
  
  def __add__(self, other):
    return Direction(self.x + other.x, self.y + other.y)
  
  def __sub__(self, other):
    return Direction(self.x - other.x, self.y - other.y)
  
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  
  def __ne__(self, other):
    return self.x != other.x or self.y != other.y
  
  def __str__(self):
    return 'Direction <{x}, {y}>'.format(
      x=self.x,
      y=self.y
    )
