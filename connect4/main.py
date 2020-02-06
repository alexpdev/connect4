from setup import build
from config import OPTIONS as kwargs

game = build(**kwargs)
game.start()
