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


class Space(RawTurtle):

    def __init__(self,screen):
        RawTurtle.__init__(self,screen)
        self.screen = screen
        self.xy = None
        self._color = None
        self.player = None
        self.col = None
        self.row = None
        self.radius = None

    @classmethod
    def create(self,**kwargs):
        screen = kwargs["screen"]
        space = Space(screen)
        space.radius = kwargs["radius"]
        space.col = kwargs["column"]
        space.row = kwargs["row"]
        space.xy = kwargs["position"]
        space.up()
        space.goto(space.xy)
        space.down()
        return space

    def first_draw(self):
        self.color("white")
        self.begin_fill()
        self.circle(self.radius)
        self.end_fill()
        self.ht()
