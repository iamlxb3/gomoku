import collections
import sys
import pickle
import os
import dill
import numpy as np
import random
import collections
from general_funcs import convert_number_to_one_hot_list

class GomukuRl:

    def _read_Q_set_from_file(self):
        is_Q_set_exist = os.path.exists(self.Q_set_path)
        if is_Q_set_exist:
            self.Q_set = pickle.load(open(self.Q_set_path, "rb"))
        else:
            self.Q_set = collections.defaultdict(lambda: 0)


    def __init__(self, board, regressor):

        self.board = board
        self.regressor = regressor
        self.regressor_path = 'gomuku_regressor'

        # config
        self.learning_rate = 0.1
        self.discount_factor = 0.5
        self.random_walk_factor = 0.3
        #

        # Q set
        self.Q_set_path = 'gomuku_g_dict'
        self.Q_set = collections.defaultdict(lambda:0)
        #

        # get action
        action_mapping_list = []
        for i in range(board.board_size):
            for j in range(board.board_size):
                action_mapping_list.append((i,j))
        self.action_mapping_list = action_mapping_list
        #

        # state_dict
        self.state_dict = {self.board.e_c: 0, 'own': 1, 'opp': -1}
        self.state_list = []

        # action
        self.action_list = []

        # reward
        self.reward_list = []

        # reward
        self.feature_list = [] # combining state and action list

        # player_list
        self.player_list = []

    def reset(self):
        self.state_list = []
        self.action_list = []
        self.player_list =[]
        self.reward_list = []
        self.feature_list = []

    def _get_current_state(self, ai):

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
                    print("Error!!")
                    sys.exit()
                one_step_state_list.append(self.state_dict[element])

        return one_step_state_list

    def save_state(self, ai):
        one_step_state_list = self._get_current_state(ai)
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
            sys.exit()

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

    def _get_feature_list(self):
        for i, state in enumerate(self.state_list):
            combined_list = self.state_list[i] + self.action_list[i]
            self.feature_list.append(combined_list)

    def update_Q_set(self):
        self._get_feature_list()
        self._read_Q_set_from_file()
        for i, one_feature in enumerate(self.feature_list):
            one_feature_tuple = tuple(one_feature)
            reward = self.reward_list[i]
            # TODO compute next_max_Q
            next_max_Q = 0
            self.Q_set[one_feature_tuple] = (1-self.learning_rate) * self.Q_set[one_feature_tuple] + \
                                       self.learning_rate*(reward + self.discount_factor*next_max_Q)

            # save Q_set
        dill.dump(self.Q_set, open(self.Q_set_path, "wb"))

    def rl_train(self):
        print ("RL regressor training...")
        self.update_Q_set()
        feature_list = list(self.Q_set.keys())
        value_list = list(self.Q_set.values())
        #print ("Q_set_value: {}".format(self.Q_set.values()))
        print ("rl_train start! sample number: {}".format(len(value_list)))
        self.regressor.regressor_train(feature_list, value_list)
        pickle.dump(self.regressor, open(self.regressor_path, "wb"))



    def predict_next_best_move(self, valid_pos_list, ai):

        is_regressor_path = os.path.exists(self.regressor_path)
        if not is_regressor_path:
            return None

        # add some randomness to the move
        random_num = random.random()
        if random_num <= self.random_walk_factor:
            print ("Random walk!")
            return None
        #



        regressor = pickle.load(open(self.regressor_path, "rb"))
        one_step_state_list = self._get_current_state(ai)
        best_value = float('-inf')
        best_pos = [0,0]

        for valid_pos in valid_pos_list:
            action_index = self.action_mapping_list.index(valid_pos)
            action_vector = convert_number_to_one_hot_list(action_index, len(self.action_mapping_list))
            combined_vector = one_step_state_list + action_vector
            combined_array = np.array(combined_vector).reshape(1,-1)
            predict_value = regressor.regressor_predict(combined_array)[0]
            if predict_value > best_value:
                best_value = predict_value
                best_pos = valid_pos

        # print ("best_value: ", best_value)
        # print ("best_pos: ", best_pos)

        return best_pos

    def delete_Q_set(self):
        os.remove(self.Q_set_path)
        return self.Q_set_path