

class Player:

    def __init__(self,num,):
        self.num = num
        self.color = color
        self.spaces = []


class Game:

    def __init__(self,board,players):
        self.board = board
        self.players = players
        self.p1,self.p2 = players
        self.turn = 1
