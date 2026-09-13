# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/Symbolcomma_ai_11112255_AP62300T.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_AP62300T(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    GND = Pin((0, -6), 4, Direction.Down)
    SW = Pin((8, 2), 4, Direction.Right)
    IN = Pin((-8, 2), 4, Direction.Left)
    FB = Pin((8, -4), 4, Direction.Right)
    EN = Pin((-8, -4), 4, Direction.Left)
    BST = Pin((8, 0), 4, Direction.Right)
    draws = [
        Polyline(0.1524, [(-8, -6), (-8, 4)]),
        Polyline(0.1524, [(8, 4), (8, -6)]),
        Polyline(0.1524, [(-8, 4), (8, 4)]),
        Polyline(0.1524, [(8, -6), (-8, -6)]),
    ]

