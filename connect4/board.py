from turtle import _Screen as Screen
from turtle import RawTurtle
from time import sleep

class Window(Screen):
    """Class to generate game window, tkcanvas subclass.
    """
    def __init__(self,color=None):
        """ Constructor for TK window.
            color {str} -- hex color string (default: {None})
        """
        super().__init__()
        self.new_game(color)

    def new_game(self,color):
        """ Starts a New Game, Redraws game board and recreates players """
        self.setup(.8,.9,0,0)
        self.width = (self.window_width()*.9)
        self.height = (self.window_height()*.9)
        self.x = self.width/2
        self.y = self.height/2
        self.font = ('Arial',20,'bold'),"#f50"
        self.winner = None
        self.bgcolor(color)
        self.start_message()
        self.delay(8)
        self.tracer(2)
        self.game_board()
        self.create_players()

    def start_message(self):
        """ Creates Pen for writing messages at the top of the window """
        self.pen = RawTurtle(self)
        self.pen.ht()
        self.pen.up()
        self.pen.color(self.font[1])
        self.pen.goto(0,self.y)
        self.pen.write("New Game",align="center",font=self.font[0])
        return

    def create_players(self):
        """ Creates 2 players for versus mode """
        player_1 = Player(1,"#f00")
        player_2 = Player(2,"#000")
        self.player = player_1
        self.players = (player_1,player_2)

    def activate_space(self,x,y):
        """
            Onclick callback: assigns the bottom most space to active player.
            Arguements: (x{int},y{int}) = window coordinates for click position.
        """

        space = self.board.find_space(x,y)
        #find the space associated with the position given by onclick method

        if space and space.state == None:
            space = self.board.check_space(space)
            self.board.animate_drop(space)
            """ if space is valid... check if it is the bottommost empty
                space in column or return the bottom space and render
                dropping animation
            """

            space.draw(color=self.player.color)
            space.state = self.player.name
            """ fill bottommost empty space with players color
                set space state to filled by active player """

            if self.board.check_winner(space):
                # check if game over
                self.draw_message(f"GAME OVER {self.player} WINS")
                return

            # switch active players
            self.player = self.players[0] if self.players[0] != self.player else self.players[1]
            self.draw_message(str(self.player) + " Turn")

        else:
            # if click is not in valid empty space player turn continues
            self.draw_message("Try Again")

    def draw_message(self,msg):
        """ Write game state update messages to top of the window """
        self.pen.clear()
        self.pen.write(msg,align="center",font=self.font[0])
        return

    @property
    def turn(self):
        return self.player

    def play(self):
        self.onclick(self.activate_space)

    def game_board(self):
        """ Calculates and generates the board object. """
        board_height = (self.height//42)*42
        board_width = (board_height*7)/6
        bx = board_width/2
        by = board_height/2
        board_corners = [(-bx,by),(-bx,-by),(bx,-by),(bx,by)]
        self.board = Board(self,board_corners,board_width,board_height,bx,by)
        return

class Player:
    """ User Player Class controlled by end user """
    def __init__(self,number,color):
        self.number = number
        self.color = color
        self.turn = 0
        self.name = "P" + str(self.number)

    def __str__(self):
        return "Player " + str(self.number)

class Board:
    """ Area of the screen dedicated to the connect 4 game board.
    """
    def __init__(self,screen,corners,width,height,x,y):
        self.corners = corners
        self.screen = screen
        self.pen = RawTurtle(screen)
        self.pen.speed(8)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.spaces = []
        self.draw()
        self.draw_spaces()

    def draw(self):
        self.pen.up()
        self.pen.goto(self.corners[-1])
        self.pen.color("#ddd")
        self.pen.down()
        self.pen.begin_fill()
        for i in self.corners:
            self.pen.goto(i)
        self.pen.ht()
        self.pen.end_fill()
        return

    def check_winner(self,space):
        r,c = space.idx
        if space.state*4 in "".join([str(i.state) for i in self.spaces[r]]):
            return True
        if space.state*4 in "".join([str(i[c].state) for i in self.spaces]):
            return True
        direct = [(-1,-1),(-1,1),(1,1),(1,-1)]
        left,right = 0,0
        for i,x in enumerate(direct):
            num = self.check_diag(space,r,c,x[0],x[1],x)
            if i%2 == 0: left += num
            else: right += num
        if left >= 3 or right >= 3:
            return True
        return False


    def check_diag(self,space,r,c,x,y,i):
        if r+x >= 0 and r+x < 6 and c+y >= 0 and c+y < 7:
            if self.spaces[r+x][c+y].state == space.state:
                return 1 + self.check_diag(space,r,c,x+i[0],y+i[1],i)
            return 0
        return 0

    def animate_drop(self,space):
        r,c = space.idx
        for i in range(r):
            self.spaces[i][c].draw()
            self.spaces[i][c].remove()
        return

    def check_space(self,space):
        r,c = space.idx
        if r == len(self.spaces)-1 or self.spaces[r+1][c].state:
            return space
        for row in range(r+1,len(self.spaces)):
            if self.spaces[row][c].state:
                return self.spaces[row-1][c]
        return self.spaces[len(self.spaces)-1][c]


    def find_space(self,x,y):
        for row in self.spaces:
            cent,rad = row[0].center, row[0].radius
            if y > cent[1] - rad and y < cent[1] + rad:
                space = self.search_row(row,x)
        return space

    def search_row(self,row,x):
        for space in row:
            x2 = space.center[0]
            if x > x2-space.radius and x < x2 + space.radius:
                return space
        return False

    def draw_spaces(self):
        row,size = [],self.width/7
        radius = (size*.9)/2
        x,y = self.corners[0]
        for j in range(6):
            for i in range(7):
                space_x = x + (size*i)
                space_y = y - (size*j)
                center = space_x+(size/2),space_y-(size/2)
                color = "#643"
                idx = (j,i)
                space = Space(self.screen,center,radius,color,idx)
                row.append(space)
            self.spaces.append(row)
            row = []

class Space(RawTurtle):
    """ circles drawn on the window for players to assign their color """
    def __init__(self,screen,center,radius,color,idx):
        RawTurtle.__init__(self,screen)
        self.window = screen
        self.center = center
        self.radius = radius
        self.state = None
        self.idx = idx
        self._bgcolor = color
        self.color(color)
        self.up()
        self.speed(5)
        self.goto(self.center[0],self.center[1]-self.radius)
        self.ht()
        self.down()
        self.draw()

    def draw(self,color=None):
        if color:
            self.fillcolor(color)
        else:
            self.fillcolor(self._bgcolor)
        self.begin_fill()
        self.circle(self.radius)
        self.end_fill()
        return

    def remove(self):
        self.clear()
        self.draw()
        return

class AI(Player):
    def __init__(self,number,color,board,window):
        super().__init__(number,color)
        self.board = board
        self.window = window

    def turn(self):
        opp = []
        for i,row in enumerate(self.board.spaces):
            for j,space in enumerate(row):
                if space.state != None and space.state != self.name:
                    opp.append((i,j))










window = Window("#643")
window.play()
window.mainloop()
