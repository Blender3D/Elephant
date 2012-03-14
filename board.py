import re
from pieces import Rook, Pawn, King, Knight, Bishop, Queen
from point import Point

class Board(object):
  def __init__(self, state=None):
    self.width = 8
    self.height = 8
    
    self.board = []
    
    self.pieces = []
    self.white_pieces = []
    self.black_pieces = []
    
    self.whites_turn = True
    
    if not state:
      self.loadState('''
        r n b q k b n r
        p p p p p p p p
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        P P P P P P P P
        R N B Q K B N R
      ''')
    else:
      self.loadState(state)
  
  def copy(self):
    return Board(str(self))
  
  def __getitem__(self, key):
    if type(key) == int:
      return self.board[key]
    elif type(key) == tuple:
      return self.board[key[1]][key[0]]
    elif type(key) == Point:
      return self.board[key.y][key.x]
    else:
      raise ValueError('Invalid board coordinate')
  
  
  def __setitem__(self, key, value):
    if type(key) == int:
      self.board[key] = value
    elif type(key) == tuple:
      self.board[key[1]][key[0]] = value
    elif type(key) == Point:
      self.board[key.y][key.x] = value
    else:
      raise ValueError('Invalid board coordinate')
  
  
  def loadState(self, state):
    state = re.split('\n+', re.sub(r'[^prnbqkPRNBQK\.\n]', '', state.strip()))
    self.state = state
    
    board = []
    
    for y, row in enumerate(state):
      new_row = []
      
      for x, square in enumerate(row):
        if square == '.':
          new_row += [None]
        else:
          for piece in [Rook, Pawn, King, Knight, Bishop, Queen]:
            if piece.character == square.lower():
              obj = piece(self, not square.islower(), Point(x, y))
              
              new_row += [obj]
              self.pieces += [obj]
              
              if not square.islower():
                self.white_pieces += [obj]
              else:
                self.black_pieces += [obj]
              
              break
      
      board += [new_row]
    
    self.board = board
  
  
  def __str__(self):
    result = []
    
    for row in self.board:
      temp_row = []
      
      for cell in row:
        if cell == None:
          temp_row += ['.']
        elif type(cell) == str:
          temp_row += [cell]
        else:
          temp_row += [cell.letter()]
      
      result += [' '.join(temp_row)]
    
    return '\n'.join(result)
