from gomoku_board import Board

class Gomoku:

    def __init__(self, board):
        self.board = board
        self.is_game_end = False

    def initialize(self):
        self.board.initialize_board()

    def ai_move(self, board):
        pass

    def human_move(self):
        pass

    def human_vs_ai(self):
        pass

    def _human_pos_input(self):
        alphabat_list = list(self.board.alphabat)
        pos_str = input("Please type chess position: ")
        pos_list = pos_str.split(',')
        pos1 = int(pos_list[0])
        pos2_str = pos_list[1]
        pos2 = int(alphabat_list.index(pos2_str))
        if pos1 > self.board.board_size - 1 or pos1 < 0 or pos2 > self.board.board_size - 1 or pos2 < 0:
            print ("Invalid input!")
            return self._human_pos_input()
        return pos1, pos2


    def check_win(self):
        winning_chess = self.board.scan_board()
        if winning_chess == self.board.O:
            print("White win!")
            self.is_game_end = True
        elif winning_chess == self.board.X:
            print ("Black win!")
            self.is_game_end = True
        else:
            pass


    def human_test(self):
        self.board.print_board()
        while not self.is_game_end:
            pos1, pos2  = self._human_pos_input()
            self.board.update_board(pos1, pos2)
            self.board.print_board()
            self.check_win()
