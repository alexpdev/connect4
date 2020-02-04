class Player:

    def __init__(self,num,**kwargs):
        self.num = num
        self.game = None
        self.board = kwargs["board"]
        self.name = "Player " + str(num)
        if num == 1:
            self.color = kwargs["p1_color"]
        else:
            self.color = kwargs["p2_color"]
        self.spaces = []

    def __str__(self):
        return self.name

    def select_space(self,x,y):
        space = self.board.find_space(x,y)
        if space and space.is_empty():
            assigned = self.board.assign(space,self)
            self.spaces.append(assigned)
            self.game.turn_end()
            return

class Game:

    def __init__(self,**kwargs):
        self.screen = kwargs["screen"]
        self.board = kwargs["board"]
        self.players = kwargs["players"]
        self.p1,self.p2 = self.players
        self.turn = 1
        self.kwargs = kwargs

    def play_turn(self):
        if self.turn == 1:
            player = self.p1
        else:
            player = self.p2
        player.select_space()

    def turn_end(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        return

    def start(self):
        self.p1.game = self
        self.p2.game = self
        func = self.playturn
        self.screen.onclick(func,1)
        self.screen.mainloop()
