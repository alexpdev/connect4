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
        return space

    def drop_token(self,space):
        bottom = self.board.drop(space,self)
        result = self.board.check_winner(bottom)
        if result: return result
        self.spaces.append(bottom)
        return None

class Game:

    def __init__(self,**kwargs):
        self.screen = kwargs["screen"]
        self.board = kwargs["board"]
        self.p1 = kwargs["players"][0]
        self.p2 = kwargs["players"][1]
        self.winner = None
        self.turn = 1

    def play(self,x,y):
        if self.turn == 1: player = self.p1
        else: player = self.p2
        space = player.select_space(x,y)
        if space and space.is_empty():
            msg = player.drop_token(space)
            if msg:
                self.winner = player
                self.draw_message(msg)
                self.turn = 0
                print(msg)
            self.turn_end()
        return

    def draw_message(self,msg):
        x,y = self.board.corners[0]
        msg.st()
        msg.goto(0,y+15)
        msg.color("cyan")
        msg.down()
        msg.write("GAME OVER!",move=False,align="center",font=("Fira Code",25,"normal"))

    def turn_end(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        return

    def start(self):
        self.p1.game = self
        self.p2.game = self
        func = self.play
        self.screen.onclick(func,1)
        self.screen.mainloop()
