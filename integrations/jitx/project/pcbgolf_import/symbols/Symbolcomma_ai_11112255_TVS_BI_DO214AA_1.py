# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_TVS_BI_DO214AA_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_TVS_BI_DO214AA(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 0, Direction.Left),
        2: Pin((4, 0), 0, Direction.Right),
    }
    draws = [
        Polyline(0.254, [(3, 0), (3, 1)]),
        Polyline(0.1524, [(-2, 0), (-1, 0)]),
        Polyline(0.254, [(3, 1), (1, 0)]),
        Polyline(0.254, [(-1, 0), (-1, -1)]),
        Polyline(0.254, [(1, 0), (3, -1)]),
        Polyline(0.254, [(1, 0), (1, -1)]),
        Polyline(0.254, [(1, 0), (-1, 1)]),
        Polyline(0.254, [(1, 1), (1.4, 1.2)]),
        Polyline(0.254, [(-1, 1), (-1, 0)]),
        Polyline(0.254, [(-1, -1), (1, 0)]),
        Polyline(0.254, [(1, -1), (0.6, -1.2)]),
        Polyline(0.1524, [(4, 0), (3, 0)]),
        Polyline(0.254, [(3, -1), (3, 0)]),
        Polyline(0.254, [(1, 1), (1, 0)]),
    ]

