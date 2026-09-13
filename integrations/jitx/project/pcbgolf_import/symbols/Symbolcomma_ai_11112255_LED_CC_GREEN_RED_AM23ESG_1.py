# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_LED_CC_GREEN_RED_AM23ESG_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Polygon, Text


class Symbolcomma_ai_11112255_LED_CC_GREEN_RED_AM23ESG(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    AR = Pin((2, 4), 2, Direction.Up)
    AG = Pin((-2, 4), 2, Direction.Up)
    C = Pin((0, 0), 2, Direction.Down)
    draws = [
        Polyline(0.254, [(3, 2), (2, 2)]),
        Polyline(0.254, [(-1, 2), (-2, 2)]),
        Polyline(0.254, [(-2, 0), (2, 0)]),
        Polyline(0.1524, [(-3.6, 3.4), (-4.7, 2.3)]),
        Polyline(0.254, [(2, 0), (2, 2)]),
        Polyline(0.254, [(2, 2), (1, 2)]),
        Polyline(0.254, [(-2, 2), (-3, 4)]),
        Polyline(0.1524, [(0.5, 2.5), (-0.6, 1.4)]),
        Polygon([
            (-4.7, 2.3),
            (-4.4, 3),
            (-4, 2.6),
            (-4.7, 2.3)]),
        Polyline(0.254, [(-2, 2), (-2, 0)]),
        Polygon([
            (-0.6, 1.4),
            (-0.3, 2.1),
            (0.1, 1.7),
            (-0.6, 1.4)]),
        Polyline(0.254, [(-1, 4), (-2, 2)]),
        Polygon([
            (-0.7, 2.3),
            (-0.4, 3),
            (0, 2.6),
            (-0.7, 2.3)]),
        Polygon([
            (-4.6, 1.4),
            (-4.3, 2.1),
            (-3.9, 1.7),
            (-4.6, 1.4)]),
        Polyline(0.254, [(3, 4), (2, 2)]),
        Polyline(0.254, [(-1, 4), (-3, 4)]),
        Polyline(0.1524, [(0.4, 3.4), (-0.7, 2.3)]),
        Polyline(0.254, [(2, 2), (1, 4)]),
        Polyline(0.254, [(-2, 2), (-3, 2)]),
        Polyline(0.254, [(3, 4), (1, 4)]),
        Polyline(0.1524, [(-3.5, 2.5), (-4.6, 1.4)]),
        Text("G", 1.19, Anchor.W).at((-3.6, 0)),
        Text("R", 1.19, Anchor.W).at((2.6, 0)),
    ]

