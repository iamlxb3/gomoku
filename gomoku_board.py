import numpy as np
import sys
import math

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
        self.alphabat = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def initialize_board(self):
        for i in range(self.board_size):
            self.board_list.append([self.e_c for x in range(self.board_size)])
        self.board_array = np.array(self.board_list, dtype=str)

    def get_valid_pos_list(self):
        valid_pos_list = []
        for i, row in enumerate(self.board_array):
            for j, col in enumerate(self.board_array):
                if self.board_array[i][j] == self.e_c:
                    valid_pos_list.append([i,j])
        return valid_pos_list

    def get_chess_pos_list(self):
        chess_pos_list = []
        for i, row in enumerate(self.board_array):
            for j, col in enumerate(self.board_array):
                if self.board_array[i][j] == self.O or self.board_array[i][j] == self.X:
                    chess_pos_list.append([i,j])
        return chess_pos_list

    def get_ai_recommended_pos_list(self):

        def compute_distance(cor1, cor2):
            distance = math.sqrt((cor1[0]-cor2[0])**2 + (cor1[1]-cor2[1])**2)
            return distance

        # :::get_ai_recommended_pos_list
        recommended_pos_list = []
        chess_pos_list = self.get_chess_pos_list()
        valid_pos_list = self.get_valid_pos_list()

        # the first position
        if not chess_pos_list:
            recommended_pos_list = [[7,7]] #center
        else:
            for valid_pos in valid_pos_list:
                for chess_pos in chess_pos_list:
                    distance = compute_distance(valid_pos, chess_pos)

                    if distance < 6:
                        recommended_pos_list.append(valid_pos)

        return recommended_pos_list


    def update_board(self, pos1, pos2, is_first):
        if is_first:
            chess = self.X
        else:
            chess = self.O

        self.board_array[pos1][pos2] = chess

    def scan_board(self):

        examine_list = [self.O, self.X]
        value_list = [0, 0] # max in-squence value for white and black chess

        this_loop_is_find_winner = False

        while not this_loop_is_find_winner:
            for I, x_qizi in enumerate(examine_list):

                # scan each row
                for row in self.board_array:
                    x_qizi_count = 0
                    for element in row:
                        if element != x_qizi and x_qizi_count < 5:
                            x_qizi_count = 0
                        elif element != x_qizi and x_qizi_count == 5:
                            value_list[I] = x_qizi_count
                            this_loop_is_find_winner = True
                        if element == x_qizi:
                            x_qizi_count += 1

                #

                # scan each column
                for col in self.board_array.T:
                    x_qizi_count = 0
                    for element in col:
                        if element != x_qizi and x_qizi_count < 5:
                            x_qizi_count = 0
                        elif element != x_qizi and x_qizi_count == 5:
                            value_list[I] = x_qizi_count
                            this_loop_is_find_winner = True
                        if element == x_qizi:
                            x_qizi_count += 1
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

                for row_list in fb_ru_array:
                    for element in row_list:
                        if element != x_qizi and x_qizi_count < 5:
                            x_qizi_count = 0
                        elif element != x_qizi and x_qizi_count == 5:
                            value_list[I] = x_qizi_count
                            this_loop_is_find_winner = True
                        if element == x_qizi:
                            x_qizi_count += 1
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

                for row_list in lu_rb_array:
                    for element in row_list:
                        if element != x_qizi and x_qizi_count < 5:
                            x_qizi_count = 0
                        elif element != x_qizi and x_qizi_count == 5:
                            value_list[I] = x_qizi_count
                            this_loop_is_find_winner = True
                        if element == x_qizi:
                            x_qizi_count += 1
            break

        # ----------------------------------------------------------------------------------------------------------
        # CHECK WINNER
        # ----------------------------------------------------------------------------------------------------------
        # expection handling
        print ("value_list: ", value_list)

        if value_list[0] >= 5 and value_list[1] >= 5:
            print ("Error! Find 2 scan value >= 5")
            sys.exit()
        #
        if value_list[0] < 0 or value_list[1] < 0:
            print("scan error!  value < 0")
            sys.exit()

        for i, value in enumerate(value_list):
            if value == 5:
                return examine_list[i]

        return None
        # ----------------------------------------------------------------------------------------------------------

    def print_board(self):
        print ('\n')
        #print ("-------------------------------------------------------")
        for i, row_list in enumerate(self.board_array):
            if i<=9:
                print(self.e_s_one, end='')
            print (i, end='')
            print (self.e_s, end='')
            print (self.e_s.join(row_list))

        # print the last row
        print(self.e_s*2,  end='')

        alphabat = self.alphabat[0:self.board_size]
        alphabat_list = list(alphabat)
        print (self.e_s.join(alphabat_list))

        print('\n')
