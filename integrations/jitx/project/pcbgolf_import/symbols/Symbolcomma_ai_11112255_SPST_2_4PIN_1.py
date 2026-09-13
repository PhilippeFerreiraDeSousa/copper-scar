# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_SPST_2_4PIN_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline, Circle


class Symbolcomma_ai_11112255_SPST_2_4PIN(Symbol):
    pin_name_size = 0
    pad_name_size = 1.2
    P = Pin((0, -2), 2, Direction.Down)
    P1 = Pin((2, -2), 2, Direction.Down)
    S = Pin((0, 2), 2, Direction.Up)
    S1 = Pin((2, 2), 2, Direction.Up)
    draws = [
        Polyline(0.254, [(-3.5, 1.5), (-2.5, 1.5)]),
        Polyline(0.1524, [(2, 2), (0, 2)]),
        Polyline(0.254, [(0, -2), (-1, 1.5)]),
        Polyline(0.254, [(0, 1.5), (0, 2)]),
        Circle(radius=0.1).at(0, 2),
        Polyline(0.1524, [(-1, 0), (-0.5, 0)]),
        Polyline(0.1524, [(-2, 0), (-1.5, 0)]),
        Polyline(0.1524, [(2, -2), (0, -2)]),
        Polyline(0.1524, [(-3.5, 0), (-2.5, 0)]),
        Polyline(0.254, [(-3.5, 0), (-3.5, -1.5)]),
        Circle(radius=0.1).at(0, -2),
        Polyline(0.254, [(-3.5, 1.5), (-3.5, 0)]),
        Polyline(0.254, [(-3.5, -1.5), (-2.5, -1.5)]),
    ]

