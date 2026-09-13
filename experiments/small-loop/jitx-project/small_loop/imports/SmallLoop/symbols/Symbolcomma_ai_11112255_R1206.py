# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/Symbolcomma_ai_11112255_R1206.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_R1206(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 2, Direction.Left),
        2: Pin((2, 0), 2, Direction.Right),
    }
    draws = [
        Polyline(0.2032, [(0.8, -0.8), (1.3, 0.8)]),
        Polyline(0.2032, [(1.3, 0.8), (1.8, -0.8)]),
        Polyline(0.2032, [(0.3, 0.8), (0.8, -0.8)]),
        Polyline(0.2032, [(-0.2, -0.8), (0.3, 0.8)]),
        Polyline(0.2032, [(-0.7, 0.8), (-0.2, -0.8)]),
        Polyline(0.2032, [(-1.2, -0.8), (-0.7, 0.8)]),
        Polyline(0.2032, [(-1.7, 0.8), (-1.2, -0.8)]),
        Polyline(0.2032, [(-2, 0), (-1.7, 0.8)]),
        Polyline(0.2032, [(1.8, -0.8), (2, 0)]),
    ]

