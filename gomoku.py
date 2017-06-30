from gomoku_board import Board
import random

class Gomoku:

    def __init__(self, board):
        self.board = board
        self.is_game_end = False

    def initialize(self):
        self.board.initialize_board()

    def _ai_move(self, is_first, is_random = False):
        pos_list = [0,0]
        if is_random:
            valid_pos_list = self.board.get_valid_pos_list()
            pos_list = random.sample(valid_pos_list,1)[0]

        pos1 = pos_list[0]
        pos2 = pos_list[1]
        self.board.update_board(pos1, pos2, is_first)

    def _human_move(self, is_first):
        pos1, pos2 = self._human_pos_input()
        pos_list = [pos1, pos2]
        valid_pos_list = self.board.get_valid_pos_list()
        if pos_list in valid_pos_list:
            self.board.update_board(pos1, pos2, is_first)
            return True
        else:
            print ("Same move is not allowed!")
            return False


    def _human_pos_input(self):
        alphabat_list = list(self.board.alphabat)
        pos_str = input("Please type chess position: ")
        pos_list = pos_str.split(',')
        pos1 = int(pos_list[0])
        pos2_str = pos_list[1]
        if pos2_str not in alphabat_list:
            print ("Invalid input!")
            return self._human_pos_input()
        pos2 = int(alphabat_list.index(pos2_str))
        if pos1 > self.board.board_size - 1 or pos1 < 0 or pos2 > self.board.board_size - 1 or pos2 < 0:
            print ("Invalid input!")
            return self._human_pos_input()
        return pos1, pos2


    def _check_win(self):
        winning_chess = self.board.scan_board()
        if winning_chess == self.board.O:
            print("White win!")
            self.is_game_end = True
            return True
        elif winning_chess == self.board.X:
            print ("Black win!")
            self.is_game_end = True
            return True
        else:
            return False


    def human_test(self):
        is_human_first = True
        self.board.print_board()
        while not self.is_game_end:
            is_move_valid = self._human_move(is_human_first)
            if not is_move_valid:
                continue
            is_win = self._check_win()
            if not is_win:
                self.board.print_board()



    def human_vs_ai(self, is_human_first = True):
        print ("Human Vs Ai!")
        is_ai_first = not is_human_first

        if not is_human_first:
            self._ai_move(is_ai_first)

        self.board.print_board()

        while not self.is_game_end:
            is_move_valid = self._human_move(is_human_first)
            if not is_move_valid:
                continue
            is_win = self._check_win()
            if is_win:
                break
            self._ai_move(is_ai_first, is_random=True)
            is_win = self._check_win()
            if is_win:
                break
            self.board.print_board()

        self.board.print_board()

