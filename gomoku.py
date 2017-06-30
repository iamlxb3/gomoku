from gomoku_board import Board

class Gomoku:

    def __init__(self, board):
        self.board = board

    def initialize(self):
        self.board.initialize_board()

    def ai_move(self, board):
        pass

    def human_move(self):
        pass

    def human_vs_ai(self):
        pass