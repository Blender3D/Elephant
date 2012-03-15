import re
from pieces import Rook, Pawn, King, Knight, Bishop, Queen
from point import Point

class Board(object):
  def __init__(self, state=None):
    self.width = 8
    self.height = 8
    
    self.board = []
    
    self.whites_turn = True
    self.white_king = None
    self.black_king = None
    
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
  
  def __delitem__(self, key):
    if type(key) == int:
      self.board[key] = None
    elif type(key) == tuple:
      self.board[key[1]][key[0]] = None
    elif type(key) == Point:
      self.board[key.y][key.x] = None
    else:
      raise ValueError('Invalid board coordinate')
  
  def white_pieces(self):
    pieces = []
    
    for row in self.board:
      for piece in row:
        if piece and piece.color:
          pieces.append(piece)
    
    return pieces
  
  def black_pieces(self):
    pieces = []
    
    for row in self.board:
      for piece in row:
        if piece and piece.color == False:
          pieces.append(piece)
    
    return pieces
  
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
              color = not square.islower()
              new_row += [piece(self, color, Point(x, y))]
              
              if piece == King:
                if color:
                  self.white_king = new_row[-1]
                else:
                  self.black_king = new_row[-1]
              
              break
      
      board += [new_row]
    
    for row in board:
      for piece in row:
        if piece:
          if piece.color:
            piece.king = self.white_king
          else:
            piece.king = self.black_king
    
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
