from gomoku import Gomoku
from gomoku_board import Board

board1 = Board()
gomoku1 = Gomoku(board1)


board1.initialize_board()
board1.update_board()
board1.print_board()