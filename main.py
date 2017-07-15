from gomoku import Gomoku
from gomoku_board import Board
from gomoku_ai import GomokuAi
from gomoku_rl import GomukuRl
from mlp_regressor import MlpRegressor_P



# --------------------------------------------------------------------------------------------------------------
# [1.] Create board
# --------------------------------------------------------------------------------------------------------------
board1 = Board()
# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------
# [2.] Build regressor
# --------------------------------------------------------------------------------------------------------------
mlp_regressor1 = MlpRegressor_P()
hidden_layer_sizes = (20,1)
tol=1e-8
learning_rate_init=0.001
mlp_regressor1.set_regressor(hidden_layer_sizes, tol=tol, learning_rate_init=learning_rate_init)
# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------
# [3.] Build RL
# --------------------------------------------------------------------------------------------------------------
gomuku_rl = GomukuRl(board1, mlp_regressor1)
# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------
# [4.] gomoku initialize
# --------------------------------------------------------------------------------------------------------------
Total_game = 2000
gomoku1 = Gomoku(board1, Total_game, gomuku_rl=gomuku_rl)
gomoku1.initialize()
# --------------------------------------------------------------------------------------------------------------




# # --------------------------------------------------------------------
# # HUMAN VS AI
# # --------------------------------------------------------------------
# ai1 = GomokuAi(name='ai', is_first=True)
# gomoku1.human_vs_ai(ai1)
# # --------------------------------------------------------------------



# --------------------------------------------------------------------
# AI VS AI
# --------------------------------------------------------------------
print ("AI VS AI, RL TRAINING START!")
ai1 = GomokuAi(name='ai1_black', is_first=True, regressor = mlp_regressor1)
ai2 = GomokuAi(name='ai2_white', is_first=False, regressor = mlp_regressor1)



for i in range(gomoku1.Total_game):
    gomoku1.initialize()
    gomoku1.ai_vs_ai(ai1, ai2, speed=20, is_print=False, is_ai_random = False)
    print ("Game playing ({}/{}) ...".format(i+1, Total_game))
    ai1.print_return_win_ratio()
    ai2.print_return_win_ratio()
    gomoku1.game_count += 1

    every_N_game = 100
    gomoku1.delete_Q_set(every_N_game)

    #　delete Q_set every 400 games



# --------------------------------------------------------------------

#gomoku1.human_test()
#gomoku1.human_vs_ai()
