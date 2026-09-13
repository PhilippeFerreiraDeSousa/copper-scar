# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_DIODE_.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_DIODE_(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    C = Pin((2, 0), 0, Direction.Right)
    A = Pin((-2, 0), 0, Direction.Left)
    draws = [
        Polyline(0.254, [(1, 0), (-1, 1)]),
        Polyline(0.254, [(1, 0), (1, -1)]),
        Polyline(0.254, [(1, 1), (1, 0)]),
        Polyline(0.254, [(-1, -1), (1, 0)]),
        Polyline(0.254, [(-1, 0), (-1, -1)]),
        Polyline(0.254, [(-1, 1), (-1, 0)]),
        Polyline(0.1524, [(-2, 0), (-1, 0)]),
        Polyline(0.1524, [(2, 0), (1, 0)]),
    ]

