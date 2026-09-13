# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_MICRO_SD_0472192001.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_MICRO_SD_0472192001(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    DAT2 = Pin((0, 8), 4, Direction.Left)
    CDDAT3 = Pin((0, 6), 4, Direction.Left)
    CMD = Pin((0, 4), 4, Direction.Left)
    VDD = Pin((0, 14), 4, Direction.Left)
    CLK = Pin((0, 2), 4, Direction.Left)
    VSS = Pin((0, 0), 4, Direction.Left)
    DAT0 = Pin((0, 12), 4, Direction.Left)
    DAT1 = Pin((0, 10), 4, Direction.Left)
    GND = Pin((8, -2), 4, Direction.Down, pin_name_size=0)
    draws = [
        Polyline(0.254, [(0, -2), (10, -2)]),
        Polyline(0.254, [(10, 16), (0, 16)]),
        Polyline(0.254, [(0, 16), (0, -2)]),
        Polyline(0.254, [(10, -2), (10, 16)]),
    ]

