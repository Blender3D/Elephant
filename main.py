import re, sys, random

from board import Board

from colorama import init, Style, Fore
init()


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
  
  print random.choice(board.pieces).draw_moves()
