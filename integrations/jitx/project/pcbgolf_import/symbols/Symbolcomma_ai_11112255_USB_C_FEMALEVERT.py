# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_USB_C_FEMALEVERT.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Text


class Symbolcomma_ai_11112255_USB_C_FEMALEVERT(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    VBUS = {
        0: Pin((-10, 12), 4, Direction.Left),
        1: Pin((-10, 10), 4, Direction.Left),
        2: Pin((10, 12), 4, Direction.Right),
        3: Pin((10, 10), 4, Direction.Right),
    }
    GND = {
        0: Pin((-10, -8), 4, Direction.Left),
        1: Pin((-10, -10), 4, Direction.Left),
        2: Pin((10, -8), 4, Direction.Right),
        3: Pin((10, -10), 4, Direction.Right),
    }
    TX1p = Pin((-10, 6), 4, Direction.Left)
    TX1n = Pin((-10, 4), 4, Direction.Left)
    CC1 = Pin((-10, 8), 4, Direction.Left)
    DA = Pin((-10, -2), 4, Direction.Left)
    D_A = Pin((-10, -4), 4, Direction.Left)
    SBU1 = Pin((-10, -6), 4, Direction.Left)
    RX2n = Pin((-10, 0), 4, Direction.Left)
    RX2p = Pin((-10, 2), 4, Direction.Left)
    TX2p = Pin((10, 2), 4, Direction.Right)
    TX2n = Pin((10, 0), 4, Direction.Right)
    CC2 = Pin((10, 8), 4, Direction.Right)
    DB = Pin((10, -4), 4, Direction.Right)
    D_B = Pin((10, -2), 4, Direction.Right)
    SBU2 = Pin((10, -6), 4, Direction.Right)
    RX1n = Pin((10, 4), 4, Direction.Right)
    RX1p = Pin((10, 6), 4, Direction.Right)
    SHIELDA = Pin((-10, -12), 4, Direction.Left)
    SHIELDB = Pin((10, -12), 4, Direction.Right, pin_name_size=0)
    draws = [
        Polyline(0.254, [(10, 16), (-10, 16)]),
        Polyline(0.254, [(10, -14), (10, 16)]),
        Polyline(0.254, [(-10, -14), (10, -14)]),
        Polyline(0.254, [(-10, 16), (-10, -14)]),
        Text("USB-C", 1.19, Anchor.W).at((-2.6, 14.2)),
    ]

