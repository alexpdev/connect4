from setup import build
from config import OPTIONS as kwargs

game = setup(**kwargs)
game.start()
