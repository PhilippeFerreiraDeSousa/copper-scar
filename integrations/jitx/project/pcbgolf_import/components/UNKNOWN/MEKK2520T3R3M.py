# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/MEKK2520T3R3M.py 
# To import this component:
#     from .components.UNKNOWN import MEKK2520T3R3M
#     u1 = MEKK2520T3R3M.MEKK2520T3R3M()
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


class RectSmdPad(Pad):
    shape = rectangle(2, 0.8)
    paste = [
        Paste(rectangle(2, 0.8)),
    ]
    soldermask = [
        Soldermask(rectangle(2, 0.8)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternL_1008(Landpattern):
    p = {
        1: RectSmdPad().at(Transform((-1, 0), 90)),
        2: RectSmdPad().at(Transform((1, 0), 90)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-1.6, -1.2), (-1.6, 1.2)])),
        Silkscreen(Polyline(0.127, [(1.6, -1.2), (-1.6, -1.2)])),
        Silkscreen(Polyline(0.127, [(-1.6, 1.2), (1.6, 1.2)])),
        Silkscreen(Polyline(0.127, [(1.6, 1.2), (1.6, -1.2)])),
    ]

    models = [
        Model3D("L_1008_2520Metric.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_L_US1008(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((0, 4), 2, Direction.Up),
        2: Pin((0, -4), 2, Direction.Down),
    }
    draws = [
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -1.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -2.99993), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -0.99993), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 0.99993), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 1.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 2.99993), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 3.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -3.00007), 1.00007, 89.99605, -89.99211)]),
    ]

class MEKK2520T3R3M(Component):
    description = ""
    mpn = "MEKK2520T3R3M"
    datasheet = ""
    reference_designator_prefix = "L"
    landpattern = LandpatternL_1008()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_L_US1008()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[2],
        }),
    ]

Device: type[MEKK2520T3R3M] = MEKK2520T3R3M
