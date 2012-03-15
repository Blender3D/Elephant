import re, sys, random

from board import Board
from point import Point
from colorama import init, Style, Fore
init()


def ask_move():
  coordinates = map(lambda x: int(x) - 1, raw_input('What piece to move? '))

  return Point(coordinates[0], 7 - coordinates[1]), Point(coordinates[2], 7 - coordinates[3])


if __name__ == '__main__':
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
    
    pieces = board.white_pieces() if board.whites_turn else board.black_pieces()
    random.shuffle(pieces)
    
    print str(board) + '\n'
    
    for piece in pieces:
      moves = piece.valid_moves()
      
      if moves:
        can_move = True
        piece.move(random.choice(moves))
        break
    
    if not can_move:
      if board.whites_turn:
        king = board.white_king
      else:
        king = board.black_king
      
      attacker = king.checking_pieces()
      
      if attacker:
        sys.exit(attacker[0].draw_moves())
      else:
        sys.exit('STALEMATE')
    
    board.whites_turn = not board.whites_turn
