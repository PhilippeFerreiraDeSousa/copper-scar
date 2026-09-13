# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_C0805_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline
from jitx.shapes.composites import rectangle
from jitx.transform import Transform


class Symbolcomma_ai_11112255_C0805(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((0, 2), 2, Direction.Up),
        2: Pin((0, 0), 2, Direction.Down),
    }
    draws = [
        Transform((0, 0.6)) * rectangle(3.2, 0.4),
        Polyline(0.1524, [(0, 2), (0, 1.6)]),
        Transform((0, 1.4)) * rectangle(3.2, 0.4),
        Polyline(0.1524, [(0, 0), (0, 0.4)]),
    ]

