# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_MCP2542FDT_E_MNY.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class Symbolcomma_ai_11112255_MCP2542FDT_E_MNY(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    TXD = Pin((-10, 0), 4, Direction.Left)
    VSS = Pin((-10, -6), 4, Direction.Left)
    VDD = Pin((-10, 4), 4, Direction.Left)
    RXD = Pin((-10, -2), 4, Direction.Left)
    VIO = Pin((10, 4), 4, Direction.Right)
    CANL = Pin((10, -2), 4, Direction.Right)
    CANH = Pin((10, 0), 4, Direction.Right)
    STBY = Pin((10, -6), 4, Direction.Right)
    EPAD = Pin((0, -8), 4, Direction.Down)
    draws = [
        Polyline(0.1524, [(-10, -8), (10, -8)]),
        Polyline(0.1524, [(10, 6), (-10, 6)]),
        Polyline(0.1524, [(-10, 6), (-10, -8)]),
        Polyline(0.1524, [(10, -8), (10, 6)]),
    ]

