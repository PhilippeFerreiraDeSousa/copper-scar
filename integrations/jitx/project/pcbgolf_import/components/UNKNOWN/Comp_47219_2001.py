# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/Comp_47219_2001.py 
# To import this component:
#     from .components.UNKNOWN import Comp_47219_2001
#     u1 = Comp_47219_2001.Comp_47219_2001()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask, Courtyard
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Polygon, Text
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


class RectSmdPad_1(Pad):
    shape = rectangle(0.7, 1.5)
    paste = [
        Paste(rectangle(0.7, 1.5)),
    ]
    soldermask = [
        Soldermask(rectangle(0.7, 1.5)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.45, 2)
    paste = [
        Paste(rectangle(1.45, 2)),
    ]
    soldermask = [
        Soldermask(rectangle(1.45, 2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0472192001(Landpattern):
    p = {
        1: RectSmdPad_1().at((-3.67, 2.6)),
        2: RectSmdPad_1().at((-4.77, 2.6)),
        3: RectSmdPad_1().at((-5.87, 2.6)),
        4: RectSmdPad_1().at((-6.97, 2.6)),
        5: RectSmdPad_1().at((-8.07, 2.6)),
        6: RectSmdPad_1().at((-9.17, 2.6)),
        7: RectSmdPad_1().at((-10.27, 2.6)),
        8: RectSmdPad_1().at((-11.37, 2.6)),
    }
    G1 = RectSmdPad_2().at((0, 0))
    G2 = RectSmdPad_2().at((0, 8.3))
    G3 = RectSmdPad_2().at((-13.75, 8.3))
    G4 = RectSmdPad_2().at((-13.75, 0))

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-13.7, 11.95), (-13.7, 9.6)])),
        Silkscreen(Polyline(0.127, [(-13.7, 11.95), (-0.05, 11.95)])),
        Silkscreen(Polyline(0.127, [(-13.7, 1.3), (-13.7, 7)])),
        Silkscreen(Polyline(0.127, [(-13.7, -2.55), (-13.7, -1.3)])),
        Silkscreen(Polyline(0.127, [(-13.7, -2.55), (-0.05, -2.55)])),
        Silkscreen(Polyline(0.127, [(-0.05, 11.95), (-0.05, 9.6)])),
        Silkscreen(Polyline(0.127, [(-0.05, 1.3), (-0.05, 7)])),
        Silkscreen(Polyline(0.127, [(-0.05, -2.55), (-0.05, -1.3)])),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-13.7, -2.6),
            (-0.1, -2.6),
            (-0.1, 11.9),
            (-13.7, 11.9)])),
    ]

    models = [
        Model3D("472192001.step",
            position=(-7, 5.2, 2),
            scale=(1, 1, 1),
            rotation=(-90, 0, 0),
        ),
    ]

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
        Text(">REF", 0.85, Anchor.W).at((0, -4)),
        Text(">VALUE", 1, Anchor.C),
        Text("pcbgolf:0472192001", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(0, -2), (10, -2)]),
        Polyline(0.254, [(10, 16), (0, 16)]),
        Polyline(0.254, [(0, 16), (0, -2)]),
        Polyline(0.254, [(10, -2), (10, 16)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class Comp_47219_2001(Component):
    description = ""
    mpn = "47219-2001"
    datasheet = ""
    reference_designator_prefix = "J2"
    landpattern = LandpatternU0472192001()
    DAT2 = Port()
    CDDAT3 = Port()
    CMD = Port()
    VDD = Port()
    CLK = Port()
    VSS = Port()
    DAT0 = Port()
    DAT1 = Port()
    GND = Port()
    symbol = Symbolcomma_ai_11112255_MICRO_SD_0472192001()
    mappings = [
        SymbolMapping({
            DAT2: symbol.DAT2, 
            CDDAT3: symbol.CDDAT3, 
            CMD: symbol.CMD, 
            VDD: symbol.VDD, 
            CLK: symbol.CLK, 
            VSS: symbol.VSS, 
            DAT0: symbol.DAT0, 
            DAT1: symbol.DAT1, 
            GND: symbol.GND
        }),
        PadMapping({
            DAT2: landpattern.p[1],
            CDDAT3: landpattern.p[2],
            CMD: landpattern.p[3],
            VDD: landpattern.p[4],
            CLK: landpattern.p[5],
            VSS: landpattern.p[6],
            DAT0: landpattern.p[7],
            DAT1: landpattern.p[8],
            GND: [
                landpattern.G4,
                landpattern.G3,
                landpattern.G2,
                landpattern.G1,
            ],
        }),
    ]

Device: type[Comp_47219_2001] = Comp_47219_2001
