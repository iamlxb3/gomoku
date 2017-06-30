import numpy as np
import sys

class Board:

    def __init__(self):
        self.board_size = 15
        self.board_list = []
        self.board_array = np.array([])
        self.e_s_one = ' '
        self.e_s = self.e_s_one*2 # empty_symbol
        self.e_c = '-'  # empty_chess
        self.O = 'O'
        self.X = 'X'

    def initialize_board(self):
        for i in range(self.board_size):
            self.board_list.append([self.e_c for x in range(self.board_size)])
        self.board_array = np.array(self.board_list, dtype=str)

    def update_board(self):
        self.board_list[3][3] = 'O'
        self.board_list[3][4] = 'X'

    def scan_board(self):

        examine_list = [self.O, self.X]
        value_list = [0, 0] # max in-squence value for white and black chess


        for I, x_qizi in enumerate(examine_list):

            # scan each row
            for row in self.board_array:
                count_value = np.count_nonzero(row == x_qizi)
                if count_value > value_list[I]:
                    value_list[I] = count_value
            #

            # scan each column
            for row in self.board_array.T:
                count_value = np.count_nonzero(row == x_qizi)
                if count_value > value_list[I]:
                    value_list[I] = count_value
            #

            # scan from left-bottom corner to right-up corner
            width = self.board_array.shape[0]
            max_index = width-1
            #

            fb_ru_list = []
            for i in range(width):

                temp_list1 = []
                temp_list2 = []
                for j in range(i + 1):
                    temp_list1.append(self.board_array[max_index - i + j, j])
                    if i != max_index:
                        temp_list2.append(self.board_array[j, max_index - i + j])
                fb_ru_list.append(temp_list1)
                if i != max_index:
                    fb_ru_list.append(temp_list2)
            #
            fb_ru_array = np.array(fb_ru_list)

            for row in fb_ru_array:
                count_value = np.count_nonzero(row == x_qizi)
                if count_value > value_list[I]:
                    value_list[I] = count_value
            #


            # scan from left-up corner to right-bottom corner
            lu_rb_list = []
            for i in range(width):
                temp_list1 = []
                temp_list2 = []
                for j in range(i + 1):
                    temp_list1.append(self.board_array[i - j, j])
                    if i != max_index:
                        temp_list2.append(self.board_array[max_index - j, max_index - i + j])
                lu_rb_list.append(temp_list1)
                if i != max_index:
                    lu_rb_list.append(temp_list2)

            #
            lu_rb_array = np.array(lu_rb_list)

            for row in lu_rb_array:
                count_value = np.count_nonzero(row == x_qizi)
                if count_value > value_list[I]:
                    value_list[I] = count_value
            #

            # expection handling
            if value_list[0] >= 5 and value_list[1] >= 5:
                print ("Error! Find 2 scan value >= 5")
                sys.exit()


            for i, value in value_list:
                if value <= 0:
                    print ("scan error! value :{}".format(value))
                    sys.exit()
                if value == 5:
                    return examine_list[i]

            return None


    def print_board(self):
        for i, row_list in enumerate(self.board_array):
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

