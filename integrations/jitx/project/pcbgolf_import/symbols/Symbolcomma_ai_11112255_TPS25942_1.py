# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_TPS25942_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_TPS25942(Symbol):
    pin_name_size = 1.2
    DMODE = Pin((0, 6), 4, Direction.Left, pin_name_size=1.2)
    PG = Pin((20, 6), 4, Direction.Right, pin_name_size=1.2)
    PGTH = Pin((20, 4), 4, Direction.Right, pin_name_size=1.2)
    VOUT = Pin((20, 16), 4, Direction.Right, pin_name_size=0)
    VIN = Pin((0, 16), 4, Direction.Left, pin_name_size=0)
    EN = Pin((0, 12), 4, Direction.Left, pin_name_size=1.2)
    OVP = Pin((0, 10), 4, Direction.Left, pin_name_size=1.2)
    ILIM = Pin((0, 4), 4, Direction.Left, pin_name_size=1.2)
    DVDT = Pin((0, 2), 4, Direction.Left, pin_name_size=1.2)
    IMON = Pin((20, 10), 4, Direction.Right, pin_name_size=1.2)
    FLT_N = Pin((20, 8), 4, Direction.Right, pin_name_size=1.2)
    GND = Pin((20, 2), 4, Direction.Right, pin_name_size=0)
    draws = [
        Polyline(0.254, [(0, 0), (20, 0)]),
        Polyline(0.254, [(20, 18), (0, 18)]),
        Polyline(0.254, [(0, 18), (0, 0)]),
        Polyline(0.254, [(20, 0), (20, 18)]),
    ]

