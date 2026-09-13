# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/SI7101DN_T1_GE3.py 
# To import this component:
#     from .components.UNKNOWN import SI7101DN_T1_GE3
#     u1 = SI7101DN_T1_GE3.SI7101DN_T1_GE3()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Text
from jitx.shapes.composites import rectangle
from jitx.transform import Transform

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


class RectSmdPad_1(Pad):
    shape = rectangle(0.99, 0.405)
    paste = [
        Paste(rectangle(0.99, 0.405)),
    ]
    soldermask = [
        Soldermask(rectangle(0.99, 0.405)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(0.76, 0.405)
    paste = [
        Paste(rectangle(0.76, 0.405)),
    ]
    soldermask = [
        Soldermask(rectangle(0.76, 0.405)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_3(Pad):
    shape = rectangle(1.725, 2.235)
    paste = [
        Paste(rectangle(1.725, 2.235)),
    ]
    soldermask = [
        Soldermask(rectangle(1.725, 2.235)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternPP_1212_8(Landpattern):
    p = {
        1: RectSmdPad_1().at((-1.4925, 0.99)),
        2: RectSmdPad_1().at((-1.4925, 0.33)),
        3: RectSmdPad_1().at((-1.4925, -0.33)),
        4: RectSmdPad_1().at((-1.4925, -0.99)),
        5: RectSmdPad_2().at((1.4925, -0.99)),
        6: RectSmdPad_2().at((1.4925, -0.33)),
        7: RectSmdPad_2().at((1.4925, 0.33)),
        8: RectSmdPad_2().at((1.4925, 0.99)),
        9: RectSmdPad_3().at((0.5, 0)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-1.65, 1.65), (1.65, 1.65)])),
        Silkscreen(Polyline(0.1524, [(-1.65, -1.65), (1.65, -1.65)])),
    ]

    models = [
        Model3D("SI7101DN-T1-GE3.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(-90, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_SIS427_VI(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    S = Pin((0, -2), 2, Direction.Down)
    G = Pin((-4, 0), 2, Direction.Left)
    D = Pin((0, 2), 2, Direction.Up)
    draws = [
        Text(">REF", 1.19, Anchor.E).at((1, -2)),
        Text(">VALUE", 1, Anchor.C).at(Transform((0, 0), 270)),
        Text("pcbgolf:PP-1212-8", 1, Anchor.C).at(Transform((0, 0), 270)),
        Text("", 1, Anchor.C).at(Transform((0, 0), 270)),
        Polyline(0.3048, [(-0.2, 0), (-0.9, 0.2)]),
        Transform((-1.9, 0)) * rectangle(0.6, 1.4),
        Transform((-1.9, 1.5)) * rectangle(0.6, 1),
        Polyline(0.1524, [(0, -1.5), (0, -2)]),
        Polyline(0.1524, [(1.5, -0.6), (1.3, -0.8)]),
        Polyline(0.3048, [(-0.9, 0), (-0.7, 0)]),
        Polyline(0.1524, [(0, 0), (-1, 0.4)]),
        Polyline(0.1524, [(-1, -0.4), (0, 0)]),
        Polyline(0.1524, [(2, -0.6), (2, 1.5)]),
        Polyline(0.3048, [(-0.9, -0.2), (-0.2, 0)]),
        Polyline(0.1524, [(2.5, 0.5), (1.5, 0.5)]),
        Polyline(0.1524, [(-1.6, -1.5), (0, -1.5)]),
        Polyline(0.1524, [(1.5, 0.5), (2, -0.6)]),
        Polyline(0.1524, [(2.5, -0.6), (2, -0.6)]),
        Polyline(0.1524, [(-3, 0), (-4, 0)]),
        Polyline(0.1524, [(0, 0), (0, -1.5)]),
        Polyline(0.254, [(-2.88, 1.9), (-2.88, -2)]),
        Polyline(0.1524, [(2, -1.5), (2, -0.6)]),
        Polyline(0.3048, [(-0.9, 0.2), (-0.9, 0)]),
        Polyline(0.1524, [(0, 1.5), (-1.58, 1.5)]),
        Transform((-1.9, -1.5)) * rectangle(0.6, 1),
        Circle(radius=0.1).at(0, -1.5),
        Polyline(0.1524, [(0, 2), (0, 1.5)]),
        Circle(radius=0.1).at(0, 1.5),
        Polyline(0.1524, [(2.5, -0.6), (2.7, -0.4)]),
        Polyline(0.1524, [(2, -0.6), (2.5, 0.5)]),
        Polyline(0.1524, [(-1, 0.4), (-1, -0.4)]),
        Polyline(0.1524, [(0, 1.5), (2, 1.5)]),
        Polyline(0.1524, [(2, -0.6), (1.5, -0.6)]),
        Polyline(0.1524, [(-0.9, 0), (-1.6, 0)]),
        Polyline(0.1524, [(2, -1.5), (0, -1.5)]),
        Text("S", 0.54394, Anchor.W).at((-1, -2.8)),
        Text("G", 0.54394, Anchor.W).at((-4, -1)),
        Text("D", 0.54394, Anchor.W).at((-1, 2)),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class SI7101DN_T1_GE3(Component):
    description = ""
    mpn = "SI7101DN-T1-GE3"
    datasheet = ""
    reference_designator_prefix = "Q1"
    landpattern = LandpatternPP_1212_8()
    S = Port()
    G = Port()
    D = Port()
    symbol = Symbolcomma_ai_11112255_SIS427_VI()
    mappings = [
        SymbolMapping({
            S: symbol.S, 
            G: symbol.G, 
            D: symbol.D
        }),
        PadMapping({
            S: [
                landpattern.p[3],
                landpattern.p[2],
                landpattern.p[1],
            ],
            G: landpattern.p[4],
            D: [
                landpattern.p[9],
                landpattern.p[8],
                landpattern.p[7],
                landpattern.p[6],
                landpattern.p[5],
            ],
        }),
    ]

Device: type[SI7101DN_T1_GE3] = SI7101DN_T1_GE3
