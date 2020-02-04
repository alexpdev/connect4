from game import Player, Game
from config import OPTIONS
from board import Board,Space
from turtle import Screen

def setup(**kwargs):
    game = get_screen(**kwargs)
    return game

def get_screen(**kwargs):
    screen = Screen()
    tracer = kwargs["tracer"]
    delay = kwargs["delay"]
    screen.tracer(tracer,delay)
    x,y = kwargs["size"]
    screen.setup(x,y,0,0)
    bgcolor = kwargs["bgcolor"]
    screen.bgcolor(bgcolor)
    return calculate_board(screen,**kwargs)

def calculate_board(screen,**kwargs):
    kwargs["screen"] = screen
    sw,sh = screen.window_width()*.8,screen.window_height()*.9
    x,y,bw,bh = sw/2,sh/2,sw,(sw*6)/7
    top,dst = -y+bh,bh/6
    corners,mid = [(-x*1.1,top),(-x*1.1,-y),(x*1.1,-y),(x*1.1,top)],dst/2
    kwargs["corners"],gap = corners,mid*.2
    kwargs["radius"] = (dst-gap)/2
    c1r1 = (-x + mid,(top - dst) + (gap/2))
    return draw_board(dst,c1r1,**kwargs)

def draw_board(dst,c1r1,**kwargs):
    kwargs = draw_spaces(dst,c1r1,**kwargs)
    board = Board(**kwargs)
    kwargs["board"] = board
    board.draw_board()
    for k,v in board.spaces.items():
        v.speed(kwargs["speed"])
        v.first_draw()
    return new_game(**kwargs)

def draw_spaces(dst,c1r1,**kwargs):
    col,row = [],[]
    spaces = {}
    for j in range(6):
        if j > 0:
            col.append(row)
            row = []
        ypos = c1r1[1]-(dst*j)
        for i in range(7):
            xpos = c1r1[0]+(dst*i)
            kwargs["dem1"] = j
            kwargs["dem2"] = i
            kwargs["position"] = (xpos,ypos)
            row.append((xpos,ypos))
            space = Space.create(**kwargs)
            spaces[(j,i)] = space
    kwargs["positions"] = col
    kwargs["spaces"] = spaces
    return kwargs

def new_game(**kwargs):
    kwargs["players"] = gen_players(**kwargs)
    game = Game(**kwargs)
    return game

def gen_players(**kwargs):
    p1 = Player(1,**kwargs)
    p2 = Player(2,**kwargs)
    return p1,p2
