from point import Point

from colorama import init, Style, Fore
init()

class Piece(object):
  def __init__(self, board=None, color=True, position=Point()):
    self.color = color
    self.color_int = -1 if self.color else 1
    
    self.has_moved = False
    self.is_pinned = False
    self.board = board
    
    self.friends = self.board.white_pieces if self.color else self.board.black_pieces
    self.enemies = self.board.black_pieces if self.color else self.board.white_pieces
    
    self.position = position
  
  def valid_moves(self):
    moves = self.moves() + self.attacks()
    valid_moves = []
    
    for move in moves:
      test_board = self.board.copy()
      test_board[self.position].move(move)
      
      if not test_board[move].king.in_check():
        valid_moves.append(move)
    
    return valid_moves
  
  def moves(self):
    return self.get_moves(self.move_directions, self.length)
  
  def attacks(self):
    return self.get_attacks(self.move_directions, self.length)
  
  def __str__(self):
    return '{color} {piece} at ({x}, {y})'.format(
      color='white' if self.color else 'black',
      piece=self.name,
      x=self.position.x,
      y=self.position.y
    )
  
  def get_moves(self, move_directions, length):
    moves = []
    
    for move in move_directions:
      position = self.position.copy()
      total_length = 0
      
      while total_length < length:
        position += move
        total_length += 1
        
        if position.in_bounds():
          square = self.board[position]
          
          if square:
            break
          else:
            moves.append(position)
        else:
          break
    
    return moves
  
  def get_attacks(self, move_directions, length):
    attacks = []
    
    for move in move_directions:
      position = self.position.copy()
      total_length = 0
      
      while total_length < length:
        position += move
        total_length += 1
        
        if position.in_bounds():
          square = self.board[position]
          
          if square:
            if square.color != self.color:
              attacks.append(position)
            
            break
        else:
          break
    
    return attacks
  
  def draw_moves(self):
    temp_board = self.board.copy()
    
    temp_board[self.position] = Fore.GREEN + self.letter() + Style.RESET_ALL
    
    for move in self.moves():
      temp_board[move] = Fore.YELLOW + '*' + Style.RESET_ALL
    
    for attack in self.attacks():
      temp_board[attack] = Fore.RED + temp_board[attack].letter() + Style.RESET_ALL
    
    return str(temp_board)
  
  def letter(self):
    character = self.character.upper() if self.color else self.character
    
    if self.color:
      character = Style.BRIGHT + character + Style.RESET_ALL
    
    return character
  
  def move(self, move):
    self.has_moved = True
    del self.board[self.position]
    
    self.position = move
    self.board[move] = self
  
  def __eq__(self, other):
    return self.letter().lower() == other.letter().lower() if other else False
  
  def __ne__(self, other):
    return self.letter().lower() != other.letter().lower() if other else False
