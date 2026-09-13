# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/DX07S024XJ1R1100.py 
# To import this component:
#     from .components.UNKNOWN import DX07S024XJ1R1100
#     u1 = DX07S024XJ1R1100.DX07S024XJ1R1100()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Cutout, Soldermask
from jitx.layerindex import Side
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Text
from jitx.shapes.composites import rectangle

import jitx
from shapely.geometry import JOIN_STYLE
from jitx.layerindex import Side
def make_mask_expansion(
    pad_shape,
    layer_func,
    amount: float | None,
    thruhole: bool
):
    if amount is None:
        amount = jitx.current.substrate.constraints.solder_mask_registration if layer_func is Soldermask \
            else 0.0  # default Paste Mask expansion amount
    mask_shape = pad_shape.to_shapely().buffer(amount, join_style=JOIN_STYLE.mitre)
    if mask_shape.is_empty:
        return []
    layers = [layer_func(mask_shape)]
    if thruhole:
        layers.append(layer_func(mask_shape, side=Side.Bottom))
    return layers

def make_soldermask (
    pad_shape,
    *,
    amount: float | None = None,
    thruhole: bool = False):
    return make_mask_expansion(pad_shape, Soldermask, amount, thruhole)

def make_pastemask (
    pad_shape,
    *,
    amount: float | None = None,
    thruhole: bool = False):
    return make_mask_expansion(pad_shape, Paste, amount, thruhole)


class CircleThPad_1(Pad):
    shape = Circle(radius=0.3)
    cutout = [
        Cutout(Circle(radius=0.2)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.3)),
        Soldermask(Circle(radius=0.3), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class CircleThPad_2(Pad):
    shape = Circle(radius=0.55)
    cutout = [
        Cutout(Circle(radius=0.3)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.55)),
        Soldermask(Circle(radius=0.55), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class RoundRectSmdPad_1(Pad):
    shape = rectangle(0.3, 1, radius=0.1125)
    paste = [
        Paste(rectangle(0.3, 1, radius=0.1125)),
    ]
    soldermask = [
        Soldermask(rectangle(0.3, 1, radius=0.1125)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RoundRectSmdPad_2(Pad):
    shape = rectangle(0.6096, 0.6096, radius=0.3048)
    paste = [
        Paste(rectangle(0.6096, 0.6096, radius=0.3048)),
    ]
    soldermask = [
        Soldermask(rectangle(0.6096, 0.6096, radius=0.3048)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RoundRectSmdPad_3(Pad):
    shape = rectangle(1.1, 1.9, radius=0.55)
    paste = [
        Paste(rectangle(1.1, 1.9, radius=0.55)),
    ]
    soldermask = [
        Soldermask(rectangle(1.1, 1.9, radius=0.55)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternDX07S024XJ1R1100(Landpattern):
    A1 = RoundRectSmdPad_1().at((-2.75, 0.61))
    A10 = RoundRectSmdPad_1().at((1.75, 0.61))
    A11 = RoundRectSmdPad_1().at((2.25, 0.61))
    A12 = RoundRectSmdPad_1().at((2.75, 0.61))
    A2 = RoundRectSmdPad_1().at((-2.25, 0.61))
    A3 = RoundRectSmdPad_1().at((-1.75, 0.61))
    A4 = RoundRectSmdPad_1().at((-1.25, 0.61))
    A5 = RoundRectSmdPad_1().at((-0.75, 0.61))
    A6 = RoundRectSmdPad_1().at((-0.25, 0.61))
    A7 = RoundRectSmdPad_1().at((0.25, 0.61))
    A8 = RoundRectSmdPad_1().at((0.75, 0.61))
    A9 = RoundRectSmdPad_1().at((1.25, 0.61))
    B1 = CircleThPad_1().at((2.8, -0.65))
    B10 = CircleThPad_1().at((-1.6, -1.35))
    B10T = RoundRectSmdPad_2().at((-1.59951, -1.3485))
    B11 = CircleThPad_1().at((-2.4, -1.35))
    B11T = RoundRectSmdPad_2().at((-2.3975, -1.35049))
    B12 = CircleThPad_1().at((-2.8, -0.65))
    B12T = RoundRectSmdPad_2().at((-2.80069, -0.65116))
    B1T = RoundRectSmdPad_2().at((2.80337, -0.6498))
    B2 = CircleThPad_1().at((2.4, -1.35))
    B2T = RoundRectSmdPad_2().at((2.39846, -1.35365))
    B3 = CircleThPad_1().at((1.6, -1.35))
    B3T = RoundRectSmdPad_2().at((1.60274, -1.34977))
    B4 = CircleThPad_1().at((1.2, -0.65))
    B4T = RoundRectSmdPad_2().at((1.20082, -0.65074))
    B5 = CircleThPad_1().at((0.8, -1.35))
    B5T = RoundRectSmdPad_2().at((0.79673, -1.34897))
    B6 = CircleThPad_1().at((0.4, -0.65))
    B6T = RoundRectSmdPad_2().at((0.40479, -0.65117))
    B7 = CircleThPad_1().at((-0.4, -0.65))
    B7T = RoundRectSmdPad_2().at((-0.40063, -0.64729))
    B8 = CircleThPad_1().at((-0.8, -1.35))
    B8T = RoundRectSmdPad_2().at((-0.79994, -1.3485))
    B9 = CircleThPad_1().at((-1.2, -0.65))
    B9T = RoundRectSmdPad_2().at((-1.20022, -0.65305))
    S1B = RoundRectSmdPad_3().at((-4.6, -1.4), on=Side.Bottom)
    S1T = RoundRectSmdPad_3().at((-4.6, -1.4))
    S1TH = CircleThPad_2().at((-4.6, -1.4))
    S2B = RoundRectSmdPad_3().at((-4.6, -4.4), on=Side.Bottom)
    S2T = RoundRectSmdPad_3().at((-4.6, -4.4))
    S2TH = CircleThPad_2().at((-4.6, -4.4))
    S3B = RoundRectSmdPad_3().at((4.6, -4.4), on=Side.Bottom)
    S3T = RoundRectSmdPad_3().at((4.6, -4.4))
    S3TH = CircleThPad_2().at((4.6, -4.4))
    S4B = RoundRectSmdPad_3().at((4.6, -1.4), on=Side.Bottom)
    S4T = RoundRectSmdPad_3().at((4.6, -1.4))
    S4TH = CircleThPad_2().at((4.6, -1.4))

    customlayer = [
        Custom(Polyline(0.1524, [(-4.695, -8.85), (4.695, -8.85)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-4.6, 1), (-4, 1)])),
        Silkscreen(Polyline(0.1524, [(-4.6, 0), (-4.6, 1)])),
        Silkscreen(Polyline(0.1524, [(4.6, 1), (4, 1)])),
        Silkscreen(Polyline(0.1524, [(4.6, 0), (4.6, 1)])),
    ]
    cutout = [
        Cutout(Circle(radius=0.375).at(-3.6, 0)),
        Cutout(Circle(radius=0.375).at(3.6, 0)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.375).at(-3.6, 0)),
        Soldermask(Circle(radius=0.375).at(-3.6, 0), side=Side.Bottom),
        Soldermask(Circle(radius=0.375).at(3.6, 0)),
        Soldermask(Circle(radius=0.375).at(3.6, 0), side=Side.Bottom),
    ]

    models = [
        Model3D("DX07S024XJ1R1100.step",
            position=(0, -3.35, 1.6),
            scale=(1, 1, 1),
            rotation=(-90, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_USB_C_FEMALE(Symbol):
    pin_name_size = 1.2
    VBUS = {
        0: Pin((-10, 12), 4, Direction.Left, pin_name_size=1.2),
        1: Pin((-10, 10), 4, Direction.Left, pin_name_size=1.2),
        2: Pin((10, 12), 4, Direction.Right, pin_name_size=0),
        3: Pin((10, 10), 4, Direction.Right, pin_name_size=0),
    }
    GND = {
        0: Pin((-10, -8), 4, Direction.Left, pin_name_size=1.2),
        1: Pin((-10, -10), 4, Direction.Left, pin_name_size=1.2),
        2: Pin((10, -8), 4, Direction.Right, pin_name_size=0),
        3: Pin((10, -10), 4, Direction.Right, pin_name_size=0),
    }
    TX1p = Pin((-10, 6), 4, Direction.Left, pin_name_size=1.2)
    TX1n = Pin((-10, 4), 4, Direction.Left, pin_name_size=1.2)
    CC1 = Pin((-10, 8), 4, Direction.Left, pin_name_size=1.2)
    DA = Pin((-10, -2), 4, Direction.Left, pin_name_size=1.2)
    D_A = Pin((-10, -4), 4, Direction.Left, pin_name_size=1.2)
    SBU1 = Pin((-10, -6), 4, Direction.Left, pin_name_size=1.2)
    RX2n = Pin((-10, 0), 4, Direction.Left, pin_name_size=1.2)
    RX2p = Pin((-10, 2), 4, Direction.Left, pin_name_size=1.2)
    TX2p = Pin((10, 2), 4, Direction.Right, pin_name_size=0)
    TX2n = Pin((10, 0), 4, Direction.Right, pin_name_size=0)
    CC2 = Pin((10, 8), 4, Direction.Right, pin_name_size=0)
    DB = Pin((10, -4), 4, Direction.Right, pin_name_size=0)
    D_B = Pin((10, -2), 4, Direction.Right, pin_name_size=0)
    SBU2 = Pin((10, -6), 4, Direction.Right, pin_name_size=0)
    RX1n = Pin((10, 4), 4, Direction.Right, pin_name_size=0)
    RX1p = Pin((10, 6), 4, Direction.Right, pin_name_size=0)
    SHIELDA = Pin((-10, -12), 4, Direction.Left, pin_name_size=0)
    SHIELDB = Pin((10, -12), 4, Direction.Right, pin_name_size=0)
    draws = [
        Text(">REF", 1.19, Anchor.W).at((-10, -16)),
        Text(">VALUE", 1, Anchor.C),
        Text("pcbgolf:DX07S024XJ1R1100", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(10, 16), (-10, 16)]),
        Polyline(0.254, [(10, -14), (10, 16)]),
        Polyline(0.254, [(-10, -14), (10, -14)]),
        Polyline(0.254, [(-10, 16), (-10, -14)]),
        Text("USB-C", 1.19, Anchor.W).at((-2.6, 14.2)),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class DX07S024XJ1R1100(Component):
    description = ""
    mpn = "DX07S024XJ1R1100"
    datasheet = ""
    reference_designator_prefix = "J3"
    landpattern = LandpatternDX07S024XJ1R1100()
    VBUS = {
        0: Port(),
        1: Port(),
        2: Port(),
        3: Port(),
    }
    GND = {
        0: Port(),
        1: Port(),
        2: Port(),
        3: Port(),
    }
    TX1p = Port()
    TX1n = Port()
    CC1 = Port()
    DA = Port()
    D_A = Port()
    SBU1 = Port()
    RX2n = Port()
    RX2p = Port()
    TX2p = Port()
    TX2n = Port()
    CC2 = Port()
    DB = Port()
    D_B = Port()
    SBU2 = Port()
    RX1n = Port()
    RX1p = Port()
    SHIELDA = Port()
    SHIELDB = Port()
    symbol = Symbolcomma_ai_11112255_USB_C_FEMALE()
    mappings = [
        SymbolMapping({
            GND[0]: symbol.GND[0], 
            TX1p: symbol.TX1p, 
            TX1n: symbol.TX1n, 
            VBUS[0]: symbol.VBUS[0], 
            CC1: symbol.CC1, 
            DA: symbol.DA, 
            D_A: symbol.D_A, 
            SBU1: symbol.SBU1, 
            VBUS[1]: symbol.VBUS[1], 
            RX2n: symbol.RX2n, 
            RX2p: symbol.RX2p, 
            GND[1]: symbol.GND[1], 
            GND[2]: symbol.GND[2], 
            TX2p: symbol.TX2p, 
            TX2n: symbol.TX2n, 
            VBUS[2]: symbol.VBUS[2], 
            CC2: symbol.CC2, 
            DB: symbol.DB, 
            D_B: symbol.D_B, 
            SBU2: symbol.SBU2, 
            VBUS[3]: symbol.VBUS[3], 
            RX1n: symbol.RX1n, 
            RX1p: symbol.RX1p, 
            GND[3]: symbol.GND[3], 
            SHIELDA: symbol.SHIELDA, 
            SHIELDB: symbol.SHIELDB
        }),
        PadMapping({
            GND[0]: landpattern.A1,
            TX1p: landpattern.A2,
            TX1n: landpattern.A3,
            VBUS[0]: landpattern.A4,
            CC1: landpattern.A5,
            DA: landpattern.A6,
            D_A: landpattern.A7,
            SBU1: landpattern.A8,
            VBUS[1]: landpattern.A9,
            RX2n: landpattern.A10,
            RX2p: landpattern.A11,
            GND[1]: landpattern.A12,
            GND[2]: [
                landpattern.B1T,
                landpattern.B1,
            ],
            TX2p: [
                landpattern.B2T,
                landpattern.B2,
            ],
            TX2n: [
                landpattern.B3T,
                landpattern.B3,
            ],
            VBUS[2]: [
                landpattern.B4T,
                landpattern.B4,
            ],
            CC2: [
                landpattern.B5T,
                landpattern.B5,
            ],
            DB: [
                landpattern.B6T,
                landpattern.B6,
            ],
            D_B: [
                landpattern.B7T,
                landpattern.B7,
            ],
            SBU2: [
                landpattern.B8T,
                landpattern.B8,
            ],
            VBUS[3]: [
                landpattern.B9T,
                landpattern.B9,
            ],
            RX1n: [
                landpattern.B10T,
                landpattern.B10,
            ],
            RX1p: [
                landpattern.B11T,
                landpattern.B11,
            ],
            GND[3]: [
                landpattern.B12T,
                landpattern.B12,
            ],
            SHIELDA: [
                landpattern.S2TH,
                landpattern.S2T,
                landpattern.S2B,
                landpattern.S1TH,
                landpattern.S1T,
                landpattern.S1B,
            ],
            SHIELDB: [
                landpattern.S4TH,
                landpattern.S4T,
                landpattern.S4B,
                landpattern.S3TH,
                landpattern.S3T,
                landpattern.S3B,
            ],
        }),
    ]

Device: type[DX07S024XJ1R1100] = DX07S024XJ1R1100
