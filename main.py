from BoxGame import BoxesGame
from Minimax import Minimax

board_size = 7

minimax = Minimax(board_size)
minimax.play()

game_instance = BoxesGame(board_size)
game_instance.mainloop()
