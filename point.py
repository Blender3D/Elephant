class Point(object):
  def __init__(self, x=None, y=None):
    self.x = x
    self.y = y
  
  def in_bounds(self):
    return 0 <= self.x <= 7 and 0 <= self.y <= 7
  
  def copy(self):
    return Point(self.x, self.y)
  
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  
  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)
  
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  
  def __ne__(self, other):
    return self.x != other.x or self.y != other.y
  
  def __str__(self):
    return 'Point ({x}, {y})'.format(
      x=self.x,
      y=self.y
    )
