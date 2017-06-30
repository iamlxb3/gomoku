import numpy as np

class Board:

    def __init__(self):
        self.board_list =[]
        self.board_size = 15
        self.e_s_one = ' '
        self.e_s = self.e_s_one*2 # empty_symbol
        self.e_c = '-'  # empty_chess

    def initialize_board(self):
        for i in range(self.board_size):
            self.board_list.append([self.e_c for x in range(self.board_size)])

    def update_board(self):
        self.board_list[3][3] = 'O'
        self.board_list[3][4] = 'X'


    def print_board(self):
        for i, row_list in enumerate(self.board_list):
            if i<=9:
                print(self.e_s_one, end='')
            print (i, end='')
            print (self.e_s, end='')
            print (self.e_s.join(row_list))

        # print the last row
        print(self.e_s*2,  end='')
        alphabat = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabat = alphabat[0:self.board_size]
        alphabat_list = list(alphabat)
        print (self.e_s.join(alphabat_list))


