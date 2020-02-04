from setup import setup
from config import OPTIONS as kwargs

game = setup(**kwargs)
game.start()
