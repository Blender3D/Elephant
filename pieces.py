# This Python file uses the following encoding: utf-8

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
  length = 2
  move_directions = [
    Direction(0, 1)
  ]
  attack_directions = [
    Direction(1, 1),
    Direction(-1, 1)
  ]
  
  def __init__(self, *arguments):
    Piece.__init__(self, *arguments)
    
    if self.position.y != (3.5 - 2.5 * self.color_int):
      self.has_moved = True
      self.length = 1
  
  def move(self, move):
    del self.board[self.position]
    
    self.position = move
    self.board[move] = self
    
    self.has_moved = True
    self.length = 1
  
  def moves(self):
    return self.get_moves(self.move_directions, self.length)
  
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
            moves.append(position)
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
  
  def in_check(self):
    for piece in self.enemies():
      if self.position in piece.attacks():
        return True
    
    return False
  
  def checking_pieces(self):
    pieces = []
    
    for piece in self.enemies():
      if self.position in piece.attacks():
        pieces.append(piece)
    
    return pieces


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
