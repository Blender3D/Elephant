import re, sys, random
from colorama import init, Style, Fore
init()

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



class Move(object):
  def __init__(self, origin=Point(), target=Point(), category='normal'):
    self.category = category
    self.origin = origin
    self.target = target


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
            moves.append(Move(self.position, position))
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
              attacks.append(Move(self.position, position))
            
            break
        else:
          break
    
    return attacks
  
  def draw_moves(self):
    temp_board = self.board.copy()
    
    temp_board[self.position] = Fore.GREEN + self.letter() + Style.RESET_ALL
    
    for move in self.moves():
      temp_board[move.target] = Fore.YELLOW + '*' + Style.RESET_ALL
    
    for attack in self.attacks():
      temp_board[attack.target] = Fore.RED + temp_board[attack].letter() + Style.RESET_ALL
    
    return str(temp_board)
  
  def letter(self):
    character = self.character.upper() if self.color else self.character
    
    if self.color:
      character = Style.BRIGHT + character + Style.RESET_ALL
    
    return character
  
  def move(self, move):
    self.has_moved = True

    if type(self.board[self.position]) == Pawn:
      self.board.fifty_move_rule_count = 0
    else:
      self.board.fifty_move_rule_count += 0.5
    
    del self.board[self.position]
    
    self.position = move.target
    
    self.board[move] = self
    self.board.last_moved_piece = self
  
  def __eq__(self, other):
    return self.letter().lower() == other.letter().lower() if other else False
  
  def __ne__(self, other):
    return self.letter().lower() != other.letter().lower() if other else False



class Rook(Piece):
  name = 'rook'
  character = 'r'
  length = 8
  value = 5.0
  move_directions = [
    Direction(0, 1),
    Direction(0, -1),
    Direction(-1, 0),
    Direction(1, 0)
  ]



class Pawn(Piece):
  name = 'pawn'
  character = 'p'
  length = 2
  value = 1.0
  move_directions = [
    Direction(0, 1)
  ]
  attack_directions = [
    Direction(1, 1),
    Direction(-1, 1)
  ]
  
  def __init__(self, *arguments):
    Piece.__init__(self, *arguments)

    self.last_move = None
    
    if self.position.y != (3.5 - 2.5 * self.color_int):
      self.has_moved = True
      self.length = 1
  
  def move(self, move):
    self.board.fifty_move_rule_count = 0
    
    del self.board[self.position]
    
    self.position = move.target
    self.board[move] = self
    
    if move.category.startswith('promote to '):
      self.board.promote(self, eval(move.category[11:].title()))

    self.board.last_moved_piece = self.board[move]

    if not self.has_moved and self.position.y == 3.5 - 0.5 * self.color_int:
      self.last_move = 'double jump'
    else:
      self.last_move = None
    
    self.has_moved = True
    self.length = 1
  
  def moves(self):
    moves = self.get_moves(self.move_directions, self.length)
    adjusted_moves = []

    last_piece = self.board.last_moved_piece

    if type(last_piece) == Pawn:
      if last_piece.last_move == 'double jump':
        if last_piece.position.y == self.position.y and abs(last_piece.position.x - self.position.x) == 1:
          moves.append(Move(self.position, self.position + Direction(last_piece.position.x - self.position.x, self.color_int), 'en passant'))
    
    for move in moves[:]:
      if move.target.y in [0, 7]:
        for piece in ['queen', 'rook', 'bishop', 'knight']:
          adjusted_moves.append(Move(self.position, move.target, 'promote to {0}'.format(piece)))
      else:
        adjusted_moves.append(move)
    
    return adjusted_moves
  
  def attacks(self):
    return self.get_attacks(self.attack_directions, 1)
  
  def get_moves(self, move_directions, length):
    moves = []
    
    for move in move_directions:
      test_move = Direction(move.x, move.y * self.color_int)
      position = self.position.copy()
      total_length = 0
      
      while total_length < length:
        position += test_move
        total_length += 1
        
        if position.in_bounds():
          square = self.board[position]
          
          if square:
            break
          else:
            moves.append(Move(self.position, position, 'double jump' if move.y == 2 else 'normal'))
        else:
          break
    
    return moves
  
  def get_attacks(self, move_directions, length):
    attacks = []
    
    for move in move_directions:
      test_move = Direction(move.x, move.y * self.color_int)
      position = self.position.copy()
      total_length = 0
      
      while total_length < length:
        position += test_move
        total_length += 1
        
        if position.in_bounds():
          square = self.board[position]
          
          if square:
            if square.color != self.color:
              attacks.append(Move(self.position, position))
            
            break
        else:
          break
    
    return attacks
  


class King(Piece):
  name = 'king'
  character = 'k'
  length = 1
  value = 0.0
  move_directions = [
    Direction(0, 1),
    Direction(0, -1),
    Direction(-1, 0),
    Direction(-1, -1),
    Direction(-1, 1),
    Direction(1, 0),
    Direction(1, -1),
    Direction(1, 1)
  ]
  
  def can_move(self):
    if self.valid_moves():
      return True
    
    for piece in self.friends():
      if piece.valid_moves():
        return True

    return False
  
  def in_checkmate(self):
    return self.in_check() and not self.can_move()
  
  def in_check(self):
    for piece in self.enemies():
      if self.position in map(lambda move: move.target, piece.attacks()):
        return True
    
    return False
  
  def checking_pieces(self):
    pieces = []
    
    for piece in self.enemies():
      if self.position in map(lambda move: move.target, piece.attacks()):
        pieces.append(piece)
    
    return pieces

  def can_checkmate(self):
    pieces = map(lambda piece: type(piece), self.friends())

    if len(pieces) == 1:
      return False
    elif len(pieces) == 2:
      if Knight in pieces or Bishop in pieces:
        return False
      else:
        return True
    elif len(pieces) == 3:
      if pieces.count(Knight) == 2:
        return False
      else:
        return True
    else:
      return True



class Knight(Piece):
  name='knight'
  character='n'
  length = 1
  value = 3.0
  move_directions = [
    Direction(1, 2),
    Direction(1, -2),
    Direction(-1, 2),
    Direction(-1, -2),
    Direction(2, 1),
    Direction(2, -1),
    Direction(-2, 1),
    Direction(-2, -1)
  ]
  


class Bishop(Piece):
  name='bishop'
  character='b'
  length = 8
  value = 3.0
  move_directions = [
    Direction(-1, -1),
    Direction(-1, 1),
    Direction(1, -1),
    Direction(1, 1)
  ]
  


class Queen(Piece):
  name='queen'
  character='q'
  length = 8
  value = 9.0
  move_directions = [
    Direction(0, 1),
    Direction(0, -1),
    Direction(-1, 0),
    Direction(-1, -1),
    Direction(-1, 1),
    Direction(1, 0),
    Direction(1, -1),
    Direction(1, 1)
  ]



class Board(object):
  def __init__(self, state=None):
    self.width = 8
    self.height = 8
    
    self.board = []
    
    self.whites_turn = True
    self.white_king = None
    self.black_king = None

    self.last_moved_piece = None
    self.fifty_move_rule_count = 0
    
    if not state:
      self.load_state('''
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
      self.load_state(state)
  
  def copy(self):
    return Board(str(self))
  
  def __getitem__(self, key):
    if type(key) == int:
      return self.board[key]
    elif type(key) == tuple:
      return self.board[key[1]][key[0]]
    elif type(key) == Point:
      return self.board[key.y][key.x]
    elif type(key) == Move:
      return self.board[key.target.y][key.target.x]
    else:
      raise ValueError('Invalid board coordinate')
  
  def __setitem__(self, key, value):
    if type(key) == int:
      self.board[key] = value
    elif type(key) == tuple:
      self.board[key[1]][key[0]] = value
    elif type(key) == Point:
      self.board[key.y][key.x] = value
    elif type(key) == Move:
      self.board[key.target.y][key.target.x] = value
    else:
      raise ValueError('Invalid board coordinate')
  
  def __delitem__(self, key):
    if type(key) == int:
      self.board[key] = None
    elif type(key) == tuple:
      self.board[key[1]][key[0]] = None
    elif type(key) == Point:
      self.board[key.y][key.x] = None
    elif type(key) == Move:
      self.board[key.target.y][key.target.x] = None
    else:
      raise ValueError('Invalid board coordinate')
  
  def promote(self, pawn, piece):
    self[pawn.position] = piece(pawn.board, pawn.color, pawn.position)
    self[pawn.position].king = pawn.king
  
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
  
  def evaluate(self, side=True):
    opponent_king, king = (self.black_king, self.white_king) if side else (self.white_king, self.black_king)
    enemies, allies = (self.black_pieces(), self.white_pieces()) if side else (self.white_pieces(), self.black_pieces())
    
    if opponent_king.in_checkmate():
      return 10000
    
    value = 0
    
    for piece in allies:
      value += piece.value
    
    for piece in enemies:
      value -= piece.value
    
    return value
    
  
  def load_state(self, state):
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
  
  def pieces(self):
    result = []
    
    for row in self.board:
      for square in row:
        if square:
          result.append(square)
    
    return result
  
  def white_pieces(self):
    result = []
    
    for piece in self.pieces():
      if piece.color == True:
        result.append(piece)
    
    return result
  
  def black_pieces(self):
    result = []
    
    for piece in self.pieces():
      if piece.color == False:
        result.append(piece)
    
    return result
  
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
  
  def is_stalemate(self):
    current_side = self.white_pieces() if self.whites_turn else self.black_pieces()
    current_king = self.white_king if self.whites_turn else self.black_king
    
    if current_king.in_check():
      return False, ''

    if not self.white_king.can_checkmate() and not self.black_king.can_checkmate():
      return True, 'No kings can checkmate'
    
    if self.fifty_move_rule_count >= 50:
      return True, 'Fifty move rule'
    
    for piece in current_side:
      if piece.valid_moves():
        return False, ''
    
    return True, 'The king is trapped but not in check'
    
      


def ask_move():
  coordinates = map(lambda x: int(x) - 1, raw_input('What piece to move? '))

  return Point(coordinates[0], 7 - coordinates[1]), Point(coordinates[2], 7 - coordinates[3])


if __name__ == '__main__':
  depth = 1
  board = Board('''
    r n b q k b n r
    p p p p p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    P P P P P P P P
    R N B Q K B N R
  ''')
  
  while True:
    can_move = False
    best_move = (None, None, None)
    
    if board.is_stalemate()[0]:
      print board
      sys.exit('STALEMATE: {0}'.format(board.is_stalemate()[1]))
    
    pieces = board.white_pieces() if board.whites_turn else board.black_pieces()
    random.shuffle(pieces)
    
    print str(board) + '\n'
    
    for piece in pieces:
      moves = piece.valid_moves()
      random.shuffle(moves)
      
      for move in moves:
        test_board = board.copy()
        test_board[piece.position].move(move)
        
        evaluation = test_board.evaluate(board.whites_turn)
        
        if best_move[0] is not None:
          if best_move[0] < evaluation:
            best_move = evaluation, piece, move
        else:
          best_move = evaluation, piece, move
    
    if best_move[0] is not None:
      best_move[1].move(best_move[2])
      raw_input()
    else:
      if board.whites_turn:
        king = board.white_king
      else:
        king = board.black_king
      
      attacker = king.checking_pieces()[0]
      
      print 'CHECKMATE'
      sys.exit(attacker.draw_moves())
      
    board.whites_turn = not board.whites_turn
