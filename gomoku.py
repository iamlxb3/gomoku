import sys
import random
import time


class Gomoku:

    def __init__(self, board, gomuku_rl = None):
        self.board = board
        self.is_game_end = False
        self.step = 0
        self.game_count = 0
        self.gomuku_rl = gomuku_rl

    def initialize(self):
        self.step = 0
        self.is_game_end = False
        self.gomuku_rl.reset()
        self.board.initialize_board()

    def _add_ai(self, ai1, ai2):
        if ai1.is_first == ai2.is_first:
            print ("Two ais have the same is_first!")
            sys.exit()
        elif ai1.name == ai2.name:
            print ("Two ais have the same name!")
            sys.exit()
        self.ai1 = ai1
        self.ai2 = ai2


    def _ai_move(self, ai, is_random = False):
        is_first = ai.is_first
        pos_list = [0,0]
        valid_pos_list = self.board.get_ai_recommended_pos_list()

        if is_random:
            pos_list = random.sample(valid_pos_list,1)[0]
        else:
            pos_list = self.gomuku_rl.predict_next_best_move(valid_pos_list, ai)

        if pos_list is None:
            pos_list = random.sample(valid_pos_list, 1)[0]

        pos1 = pos_list[0]
        pos2 = pos_list[1]
        self.board.update_board(pos1, pos2, is_first)
        ai.latest_action = [pos1, pos2]

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
        try:
            pos1 = int(pos_list[0])
        except ValueError:
            print ("Invalid input!")
            return self._human_pos_input()
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
            return True, winning_chess
        elif winning_chess == self.board.X:
            print ("Black win!")
            self.is_game_end = True
            return True, winning_chess
        else:
            return False,''


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


    def human_vs_ai(self, ai, is_human_first = True):


        print ("Human Vs Ai!")
        is_ai_first = not is_human_first
        ai.is_first = is_ai_first

        if not is_human_first:
            self._ai_move(ai)

        self.board.print_board()

        while not self.is_game_end:
            is_move_valid = self._human_move(is_human_first)
            if not is_move_valid:
                continue
            is_win = self._check_win()
            if is_win:
                break
            self._ai_move(ai, is_random=True)
            is_win = self._check_win()
            if is_win:
                break
            self.board.print_board()

        self.board.print_board()



    def ai_vs_ai(self, ai1, ai2, speed = 1, is_print = False, is_ai_random = True):

        # (0.) add ai
        self._add_ai(ai1, ai2)

        # (1.) clear and add max step
        self.step=0
        max_step = self.board.board_size**2
        #

        if ai1.is_first:
            first_move_ai = ai1
            second_move_ai = ai2
        else:
            first_move_ai = ai2
            second_move_ai = ai1

        while not self.is_game_end:
            time.sleep(1/speed)
            # RL-SAVE STATE
            self.gomuku_rl.save_state(first_move_ai)
            self._ai_move(first_move_ai, is_random=is_ai_random)
            # RL-SAVE ACTION
            self.gomuku_rl.save_action(first_move_ai)
            # ----------------------------------------------------------------------------------------------------------
            # CHECK WIN
            # ----------------------------------------------------------------------------------------------------------
            is_win, winning_chess = self._check_win()
            if is_win:
                # record winning rate
                if winning_chess == self.board.X:
                    first_move_ai.win_lose_list[0] += 1
                    second_move_ai.win_lose_list[1] += 1
                elif winning_chess == self.board.O:
                    second_move_ai.win_lose_list[0] += 1
                    first_move_ai.win_lose_list[1] += 1
                break
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            # add step
            # ----------------------------------------------------------------------------------------------------------
            self.step += 1
            if self.step == max_step:
                print ("Draw! No one wins")
                break
            #
            # ----------------------------------------------------------------------------------------------------------

            if is_print:
                self.board.print_board()


            time.sleep(1/speed)
            # RL-SAVE STATE
            self.gomuku_rl.save_state(second_move_ai)
            self._ai_move(second_move_ai, is_random=is_ai_random)
            # RL-SAVE ACTION
            self.gomuku_rl.save_action(second_move_ai)
            # ----------------------------------------------------------------------------------------------------------
            # CHECK WIN
            # ----------------------------------------------------------------------------------------------------------
            is_win, winning_chess = self._check_win()
            if is_win:
                # record winning rate
                if winning_chess == self.board.X:
                    first_move_ai.win_lose_list[0] += 1
                    second_move_ai.win_lose_list[1] += 1
                elif winning_chess == self.board.O:
                    second_move_ai.win_lose_list[0] += 1
                    first_move_ai.win_lose_list[1] += 1
                break
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            # add step
            # ----------------------------------------------------------------------------------------------------------
            self.step += 1
            if self.step == max_step:
                print ("Draw! No one wins")
                winning_chess = None
                break
            # ----------------------------------------------------------------------------------------------------------

            if is_print:
                self.board.print_board()

        # print win image
        if is_print:
            self.board.print_board()

        # RL-SAVE-REWARD
        self.gomuku_rl.get_reward(winning_chess)


        # RL-TRAINING
        self.gomuku_rl.rl_train()
        #


