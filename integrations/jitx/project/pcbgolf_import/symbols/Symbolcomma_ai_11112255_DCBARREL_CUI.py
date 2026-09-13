# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_DCBARREL_CUI.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline


class Symbolcomma_ai_11112255_DCBARREL_CUI(Symbol):
    pin_name_size = 0
    pad_name_size = 1.2
    PWR = Pin((0, 2), 2, Direction.Right)
    GND = Pin((0, -2), 2, Direction.Right)
    GNDBREAK = Pin((0, 0), 2, Direction.Right)
    draws = [
        Polyline(0.254, [(0, 1.5), (-3.5, 1.5)]),
        Polyline(0.1524, [(0, 0), (0, -2)]),
        Polyline(0.254, [(0, 2.5), (0, 1.5)]),
        Polyline(0.254, [(0, 2.5), (-3.5, 2.5)]),
        Polyline(0.254, [(-2, -1), (-1, -2)]),
        Polyline(0.254, [(-3, -2), (-2, -1)]),
        ArcPolyline(0.254, [
            Arc((-3.5, 2), 0.5, 270, -180)]),
        Polyline(0.254, [(-4, -2), (-3, -2)]),
        Polyline(0.254, [(0, -2), (-1, -2)]),
    ]

