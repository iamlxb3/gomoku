import collections
import sys
from general_funcs import convert_number_to_one_hot_list

class GomukuRl:

    def __init__(self, board):

        self.board = board
        # config
        self.learning_rate = 0.1
        self.discount_factor = 0.5
        #


        # get action
        action_mapping_list = []
        for i in range(board.board_size):
            for j in range(board.board_size):
                action_mapping_list.append([i,j])
        self.action_mapping_list = action_mapping_list
        #

        # state_dict
        self.state_dict = {self.board.e_c: 0, 'own': 1, 'opp': -1}
        self.state_list = []

        # action
        self.action_list = []

        # reward
        self.reward_list = []

        # player_list
        self.player_list = []

    def reset(self):
        self.state_list = []
        self.action_list = []
        self.reward_list = []


    def save_state(self, ai):
        one_step_state_list = []
        for col in self.board.board_array.T:
            for element in col:
                if element == self.board.e_c:
                    pass
                elif element == self.board.X:
                    if ai.is_first:
                        element = 'own'
                    else:
                        element = 'opp'
                elif element == self.board.O:
                    if ai.is_first:
                        element = 'opp'
                    else:
                        element = 'own'
                else:
                    print ("Error!!")
                    sys.exit()
                one_step_state_list.append(self.state_dict[element])

        self.state_list.append(one_step_state_list)
        self.player_list.append(ai.is_first)

    def save_action(self, ai):
        action = ai.latest_action
        action_index = self.action_mapping_list.index(action)
        action_one_hot = convert_number_to_one_hot_list(action_index, len(self.action_mapping_list))
        self.action_list.append(action_one_hot)
        # check play_list
        if self.player_list[-1] == ai.is_first:
            pass
        else:
            print ("Error, state and action do not match!")
            sys.exit()



    def get_reward(self, winning_chess):

        # check the state and action list are the same length
        if len(self.player_list) == len(self.state_list) == len(self.action_list) and len(self.action_list) != 0:
            pass
        else:
            print ("length of player list, state list and actions list is not equal or list is empty!")

        for is_first in self.player_list:
            if winning_chess is None:
                reward = 0
            elif is_first and winning_chess == self.board.X:
                reward = 1
            elif is_first and winning_chess == self.board.O:
                reward = -1
            elif not is_first and winning_chess == self.board.O:
                reward = 1
            elif not is_first and winning_chess == self.board.X:
                reward = -1
            self.reward_list.append(reward)




    def pickle_Q(self):
        pass

    def pickle_func_approximator(self):
        pass