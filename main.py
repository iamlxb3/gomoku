from gomoku import Gomoku
from gomoku_board import Board

board1 = Board()
gomoku1 = Gomoku(board1)

gomoku1.initialize()
#gomoku1.human_test()
gomoku1.human_vs_ai()