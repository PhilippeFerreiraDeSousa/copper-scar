# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/Symbolcomma_ai_11112255_CREE_RGB_CLVBA.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_CREE_RGB_CLVBA(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    Rn = Pin((-8, 4), 4, Direction.Left)
    COMp = Pin((-8, -4), 4, Direction.Left)
    Bn = Pin((6, -4), 4, Direction.Right)
    Gn = Pin((6, 4), 4, Direction.Right)
    draws = [
        Polyline(0.254, [(-8, -8), (6, -8)]),
        Polyline(0.254, [(6, 8), (-8, 8)]),
        Polyline(0.254, [(-8, 8), (-8, -8)]),
        Polyline(0.254, [(6, -8), (6, 8)]),
    ]

