# -*- coding utf8 -*-
# /env/bin/python
from turtle import Screen,RawTurtle

class Board:

    def __init__(self,**kwargs):
        self.name = "connect_4"
        self.screen =    kwargs["screen"]
        self.color =     kwargs["board_color"]
        self.corners =   kwargs["corners"]
        self.pos =       kwargs["positions"]
        self.spaces =    kwargs["spaces"]
        self.turt =      None

    def draw_board(self):
        turt = RawTurtle(self.screen)
        turt.color(self.color)
        turt.up()
        turt.goto(self.corners[0])
        turt.down()
        turt.begin_fill()
        for i in self.corners:
            turt.goto(i)
        turt.goto(self.corners[0])
        turt.end_fill()
        turt.ht()
        self.turt = turt

    def find_space(self,x,y):
        for space in self.spaces.values():
            sx,sy = space.center
            r = space.radius
            if x >= sx-r and x <= sx+r:
                if y >= sy-r and y <= sy+r:
                    return space
        return None

    def assign(self,space,player):
        assigned = self.column_bottom(space)
        assigned.assign(player)
        return assigned

    def column_bottom(self,space):
        col = [i for i in self.spaces.keys() if i[1] == space.dem2]
        bottom = (space.dem1,space.dem2)
        for area in col:
            temp = self.spaces[area]
            if temp.is_empty() and temp.dem1 > bottom[0]:
                bottom = (temp.dem1,temp.dem2)
        return self.spaces[bottom]

class Space(RawTurtle):

    def __init__(self,screen):
        RawTurtle.__init__(self,screen)
        self.screen = screen
        self.xy = None
        self._color = None
        self.player = None
        self.dem1 = None
        self.dem2 = None
        self.radius = None

    @property
    def center(self):
        x,y = self.xy
        mid = x,y+self.radius
        return mid

    @classmethod
    def create(self,**kwargs):
        screen = kwargs["screen"]
        space = Space(screen)
        space.radius = kwargs["radius"]
        space.dem1 = kwargs["dem1"]
        space.dem2 = kwargs["dem2"]
        space.xy = kwargs["position"]
        space.up()
        space.goto(space.xy)
        space.down()
        return space

    def assign(self,player):
        self.player = player
        self._color = player.color
        self.draw()

    def draw(self):
        self.color(self._color)
        self.down()
        self.begin_fill()
        self.circle(self.radius)
        self.end_fill()
        return True

    def first_draw(self):
        self.color("white")
        self.begin_fill()
        self.circle(self.radius)
        self.end_fill()
        self.ht()

    def is_empty(self):
        if not self.player:
            return True
        return False
