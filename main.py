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
ai1 = GomokuAi(name='ai1', is_first=True)
ai2 = GomokuAi(name='ai2', is_first=False)
gomoku1.ai_vs_ai(ai1, ai2, speed=20, is_print=True)
# --------------------------------------------------------------------

#gomoku1.human_test()
#gomoku1.human_vs_ai()
