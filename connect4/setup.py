from config import OPTIONS
from board import Board,Space
from turtle import Screen

def setup(**kwargs):
    screen = get_screen(**kwargs)

def get_screen(**kwargs):
    screen = Screen()
    screen.tracer(1,10)
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
    draw_board(dst,c1r1,**kwargs)


def draw_board(dst,c1r1,**kwargs):
    skeys = draw_spaces(dst,c1r1,**kwargs)
    board = Board(**skeys)
    board.draw_board()
    for k,v in board.spaces.items():
        v.speed(5)
        v.first_draw()
    skeys["screen"].mainloop()

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
            kwargs["column"] = i
            kwargs["row"] = j
            kwargs["position"] = (xpos,ypos)
            row.append((xpos,ypos))
            space = Space.create(**kwargs)
            spaces[(i,j)] = space
    kwargs["positions"] = col
    kwargs["spaces"] = spaces
    return kwargs

def gen_players(**kwargs):
    pass

setup(**OPTIONS)
