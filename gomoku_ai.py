class GomokuAi:
    def __init__(self, name, is_first, regressor = None):
        self.name = name
        self.is_first = is_first
        self.win_lose_list = [0,0]
        self.latest_action = []
        self.regressor = regressor

    def print_return_win_ratio(self):
        if self.win_lose_list[0] + self.win_lose_list[1] == 0:
            win_ratio = 0.0
        else:
            win_ratio = self.win_lose_list[0]/(self.win_lose_list[0] + self.win_lose_list[1])
        print ("AI: {}, Win_ratio: {:.3f}".format(self.name, win_ratio))
        return win_ratio
