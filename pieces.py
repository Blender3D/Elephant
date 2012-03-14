from piece import Piece
from direction import Direction

class Rook(Piece):
  name = 'rook'
  character = 'r'
  length = 8
  move_directions = [
    Direction(0, 1),
    Direction(0, -1),
    Direction(-1, 0),
    Direction(1, 0)
  ]



class Pawn(Piece):
  name = 'pawn'
  character = 'p'
  length = 1
  move_directions = [
    Direction(0, 1),
    Direction(0, 2)
  ]
  attack_directions = [
    Direction(1, 1),
    Direction(-1, 1)
  ]
  
  def attacks(self):
    return self.get_attacks(self.attack_directions, self.length)
  
  def get_moves(self, move_directions, length):
    moves = []
    
    for move in move_directions:
      position = self.position.copy()
      total_length = 0
      
      while total_length < length:
        move.y *= self.color_int
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
        move.y *= self.color_int
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
  


class King(Piece):
  name = 'king'
  character = 'k'
  length = 1
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
  


class Knight(Piece):
  name='knight'
  character='n'
  length = 1
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
