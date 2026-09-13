# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/comma_ai_11112255_M2X4.py 
# To import this component:
#     from .components.UNKNOWN import comma_ai_11112255_M2X4
#     u1 = comma_ai_11112255_M2X4.comma_ai_11112255_M2X4()
from jitx.landpattern import Landpattern, Pad
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Cutout, Soldermask
from jitx.layerindex import Side
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Arc, ArcPolyline, Text
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


class CircleThPad(Pad):
    shape = Circle(radius=0.9398)
    cutout = [
        Cutout(Circle(radius=0.508)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.9398)),
        Soldermask(Circle(radius=0.9398), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class RectThPad(Pad):
    shape = rectangle(1.8796, 1.8796)
    cutout = [
        Cutout(Circle(radius=0.508)),
    ]
    soldermask = [
        Soldermask(rectangle(1.8796, 1.8796)),
        Soldermask(rectangle(1.8796, 1.8796), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class LandpatternU2X04(Landpattern):
    p = {
        1: RectThPad().at(Transform((-3.81, -1.27), 90)),
        2: CircleThPad().at(Transform((-3.81, 1.27), 90)),
        3: CircleThPad().at(Transform((-1.27, -1.27), 90)),
        4: CircleThPad().at(Transform((-1.27, 1.27), 90)),
        5: CircleThPad().at(Transform((1.27, -1.27), 90)),
        6: CircleThPad().at(Transform((1.27, 1.27), 90)),
        7: CircleThPad().at(Transform((3.81, -1.27), 90)),
        8: CircleThPad().at(Transform((3.81, 1.27), 90)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-4.699, -2.54), (4.699, -2.54)])),
        Silkscreen(Polyline(0.1524, [(-5.08, 2.159), (-5.08, -2.159)])),
        Silkscreen(Polyline(0.1524, [(5.08, 2.159), (5.08, -2.159)])),
        Silkscreen(Polyline(0.1524, [(-4.699, 2.54), (4.699, 2.54)])),
        Silkscreen(ArcPolyline(0.1524, [
            Arc((-4.699, -2.159), 0.381, 270.00016, -90.00032)])),
        Silkscreen(ArcPolyline(0.1524, [
            Arc((4.699, -2.159), 0.381, 0.00016, -90.00032)])),
        Silkscreen(ArcPolyline(0.1524, [
            Arc((-4.699, 2.159), 0.381, 180.00016, -90.00032)])),
        Silkscreen(ArcPolyline(0.1524, [
            Arc((4.699, 2.159), 0.381, 90.00016, -90.00032)])),
    ]

class Symbolcomma_ai_11112255_M2X4(Symbol):
    pin_name_size = 0
    pad_name_size = 1.2
    p = {
        1: Pin((-2, 8), 4, Direction.Left),
        2: Pin((2, 8), 4, Direction.Right),
        3: Pin((-2, 6), 4, Direction.Left),
        4: Pin((2, 6), 4, Direction.Right),
        5: Pin((-2, 4), 4, Direction.Left),
        6: Pin((2, 4), 4, Direction.Right),
        7: Pin((-2, 2), 4, Direction.Left),
        8: Pin((2, 2), 4, Direction.Right),
    }
    draws = [
        Text(">REF", 1.19, Anchor.S).at((0, 11)),
        Text(">VALUE", 1.19, Anchor.S).at((0, -2)),
        Text("pcbgolf:2X04", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.6096, [(1, 2), (2, 2)]),
        Polyline(0.4064, [(3, 0), (-3, 0)]),
        Polyline(0.6096, [(1, 4), (2, 4)]),
        Polyline(0.6096, [(1, 6), (2, 6)]),
        Polyline(0.6096, [(1, 8), (2, 8)]),
        Polyline(0.6096, [(-1, 2), (-2, 2)]),
        Polyline(0.6096, [(-1, 4), (-2, 4)]),
        Polyline(0.6096, [(-1, 6), (-2, 6)]),
        Polyline(0.4064, [(3, 0), (3, 10)]),
        Polyline(0.4064, [(-3, 10), (-3, 0)]),
        Polyline(0.4064, [(-3, 10), (3, 10)]),
        Polyline(0.6096, [(-1, 8), (-2, 8)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class comma_ai_11112255_M2X4(Component):
    description = ""
    mpn = "comma.ai_11112255_M2X4"
    datasheet = ""
    reference_designator_prefix = "J4"
    landpattern = LandpatternU2X04()
    p = {
        1: Port(),
        2: Port(),
        3: Port(),
        4: Port(),
        5: Port(),
        6: Port(),
        7: Port(),
        8: Port(),
    }
    symbol = Symbolcomma_ai_11112255_M2X4()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2], 
            p[3]: symbol.p[3], 
            p[4]: symbol.p[4], 
            p[5]: symbol.p[5], 
            p[6]: symbol.p[6], 
            p[7]: symbol.p[7], 
            p[8]: symbol.p[8]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[2],
            p[3]: landpattern.p[3],
            p[4]: landpattern.p[4],
            p[5]: landpattern.p[5],
            p[6]: landpattern.p[6],
            p[7]: landpattern.p[7],
            p[8]: landpattern.p[8],
        }),
    ]

Device: type[comma_ai_11112255_M2X4] = comma_ai_11112255_M2X4
