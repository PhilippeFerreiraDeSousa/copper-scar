# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/MCP2542FDT_H_MNY.py 
# To import this component:
#     from .components.UNKNOWN import MCP2542FDT_H_MNY
#     u1 = MCP2542FDT_H_MNY.MCP2542FDT_H_MNY()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline
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
    shape = rectangle(0.7572, 0.2548)
    paste = [
        Paste(rectangle(0.7572, 0.2548)),
    ]
    soldermask = [
        Soldermask(rectangle(0.7572, 0.2548)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.6002, 1.6002)
    paste = [
        Paste(rectangle(1.6002, 1.6002)),
    ]
    soldermask = [
        Soldermask(rectangle(1.6002, 1.6002)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternTDFN8_2X3MC_MCH(Landpattern):
    p = {
        1: RectSmdPad_1().at((-1.42, 0.75)),
        2: RectSmdPad_1().at((-1.42, 0.25)),
        3: RectSmdPad_1().at((-1.42, -0.25)),
        4: RectSmdPad_1().at((-1.42, -0.75)),
        5: RectSmdPad_1().at((1.42, -0.75)),
        6: RectSmdPad_1().at((1.42, -0.25)),
        7: RectSmdPad_1().at((1.42, 0.25)),
        8: RectSmdPad_1().at((1.42, 0.75)),
    }
    PAD = RectSmdPad_2().at((0, 0))

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(1.4986, 1.016), (0.3048, 1.016)])),
        Silkscreen(Polyline(0.1524, [(0.3048, 1.016), (-1.4986, 1.016)])),
        Silkscreen(Polyline(0.1524, [(-1.4986, 1.016), (-1.4986, -1.016)])),
        Silkscreen(Polyline(0.1524, [(1.4986, -1.016), (1.4986, 1.016)])),
        Silkscreen(Polyline(0.1524, [(-1.4986, -1.016), (1.4986, -1.016)])),
        Silkscreen(ArcPolyline(0.1524, [
            Arc((-0, 1.0033), 0.30506, 2.38594, -180)])),
    ]

    models = [
        Model3D("DFN-8-1EP_3x2mm_P0.5mm_EP1.7x1.6mm.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

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

class MCP2542FDT_H_MNY(Component):
    description = ""
    mpn = "MCP2542FDT-H/MNY"
    datasheet = ""
    reference_designator_prefix = "U"
    landpattern = LandpatternTDFN8_2X3MC_MCH()
    TXD = Port()
    VSS = Port()
    VDD = Port()
    RXD = Port()
    VIO = Port()
    CANL = Port()
    CANH = Port()
    STBY = Port()
    EPAD = Port()
    symbol = Symbolcomma_ai_11112255_MCP2542FDT_E_MNY()
    mappings = [
        SymbolMapping({
            TXD: symbol.TXD, 
            VSS: symbol.VSS, 
            VDD: symbol.VDD, 
            RXD: symbol.RXD, 
            VIO: symbol.VIO, 
            CANL: symbol.CANL, 
            CANH: symbol.CANH, 
            STBY: symbol.STBY, 
            EPAD: symbol.EPAD
        }),
        PadMapping({
            TXD: landpattern.p[1],
            VSS: landpattern.p[2],
            VDD: landpattern.p[3],
            RXD: landpattern.p[4],
            VIO: landpattern.p[5],
            CANL: landpattern.p[6],
            CANH: landpattern.p[7],
            STBY: landpattern.p[8],
            EPAD: landpattern.PAD,
        }),
    ]

Device: type[MCP2542FDT_H_MNY] = MCP2542FDT_H_MNY
