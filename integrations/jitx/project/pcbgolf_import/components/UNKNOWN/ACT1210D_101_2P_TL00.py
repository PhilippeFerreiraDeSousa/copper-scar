# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/ACT1210D_101_2P_TL00.py 
# To import this component:
#     from .components.UNKNOWN import ACT1210D_101_2P_TL00
#     u1 = ACT1210D_101_2P_TL00.ACT1210D_101_2P_TL00()
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


class RectSmdPad(Pad):
    shape = rectangle(1.05, 1.05)
    paste = [
        Paste(rectangle(1.05, 1.05)),
    ]
    soldermask = [
        Soldermask(rectangle(1.05, 1.05)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternCHOKE_3_2X2_5(Landpattern):
    p = {
        1: RectSmdPad().at((-1.5, 0.725)),
        2: RectSmdPad().at((-1.5, -0.725)),
        3: RectSmdPad().at((1.5, -0.725)),
        4: RectSmdPad().at((1.5, 0.725)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.65, 1.3), (1.65, -1.3)])),
        Silkscreen(Polyline(0.127, [(-1.65, 1.3), (1.65, 1.3)])),
        Silkscreen(Polyline(0.127, [(1.65, -1.3), (-1.65, -1.3)])),
        Silkscreen(Polyline(0.127, [(-1.65, -1.3), (-1.65, 1.3)])),
    ]

    models = [
        Model3D("ACT1210D-101-2P-TL00.step",
            position=(11.4, -7.4, 1.2),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_ACT1210D_CHOKE(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-4, 2), 2, Direction.Left),
        2: Pin((-4, -2), 2, Direction.Left),
        3: Pin((4, -2), 2, Direction.Right),
        4: Pin((4, 2), 2, Direction.Right),
    }
    draws = [
        ArcPolyline(0.2032, [
            Arc((3.19993, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-2.79993, -2.00007), 1.00007, 179.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((3.20007, -2.00007), 1.00007, 179.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((3.19993, 2.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.79993, 2.00007), 1.00007, 269.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.80007, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((1.20007, -2.00007), 1.00007, 179.99605, -89.99211)]),
        Polyline(0.2032, [(4.2, -0.4), (-3.8, -0.4)]),
        ArcPolyline(0.2032, [
            Arc((1.20007, 2.00007), 1.00007, 269.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.79993, -2.00007), 1.00007, 179.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((3.20007, 2.00007), 1.00007, 269.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((1.19993, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((1.19993, 2.00007), 1.00007, 359.99605, -89.99211)]),
        Polyline(0.2032, [(4.2, 0.4), (-3.8, 0.4)]),
        ArcPolyline(0.2032, [
            Arc((-2.80007, 2.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.80007, 2.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-2.80007, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-2.79993, 2.00007), 1.00007, 269.99605, -89.99211)]),
    ]

class ACT1210D_101_2P_TL00(Component):
    description = ""
    mpn = "ACT1210D-101-2P-TL00"
    datasheet = ""
    reference_designator_prefix = "L"
    landpattern = LandpatternCHOKE_3_2X2_5()
    p = {
        1: Port(),
        2: Port(),
        3: Port(),
        4: Port(),
    }
    symbol = Symbolcomma_ai_11112255_ACT1210D_CHOKE()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2], 
            p[3]: symbol.p[3], 
            p[4]: symbol.p[4]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[2],
            p[3]: landpattern.p[3],
            p[4]: landpattern.p[4],
        }),
    ]

Device: type[ACT1210D_101_2P_TL00] = ACT1210D_101_2P_TL00
