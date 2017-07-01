from gomoku import Gomoku
from gomoku_board import Board
from gomoku_ai import GomokuAi

board1 = Board()
gomoku1 = Gomoku(board1)

gomoku1.initialize()

# # --------------------------------------------------------------------
# # HUMAN VS AI
# # --------------------------------------------------------------------
# ai1 = GomokuAi(name='ai', is_first=True)
# gomoku1.human_vs_ai(ai1)
# # --------------------------------------------------------------------



# --------------------------------------------------------------------
# AI VS AI
# --------------------------------------------------------------------
ai1 = GomokuAi(name='ai1_black', is_first=True)
ai2 = GomokuAi(name='ai2_white', is_first=False)

Total_game = 10
for i in range(Total_game):
    gomoku1.initialize()
    gomoku1.ai_vs_ai(ai1, ai2, speed=20, is_print=True)
    print ("Game playing ({}/{}) ...".format(i+1, Total_game))
    ai1.print_return_win_ratio()
    ai2.print_return_win_ratio()
    gomoku1.game_count += 1



# --------------------------------------------------------------------

#gomoku1.human_test()
#gomoku1.human_vs_ai()
