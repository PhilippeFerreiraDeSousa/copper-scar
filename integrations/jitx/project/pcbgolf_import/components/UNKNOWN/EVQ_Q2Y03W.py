# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/EVQ_Q2Y03W.py 
# To import this component:
#     from .components.UNKNOWN import EVQ_Q2Y03W
#     u1 = EVQ_Q2Y03W.EVQ_Q2Y03W()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
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

def make_pastemask (
    pad_shape,
    *,
    amount: float | None = None,
    thruhole: bool = False):
    return make_mask_expansion(pad_shape, Paste, amount, thruhole)


class RectSmdPad(Pad):
    shape = rectangle(3.2, 1.2)
    paste = [
        Paste(rectangle(3.2, 1.2)),
    ]
    soldermask = [
        Soldermask(rectangle(3.2, 1.2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternEVQ_Q2(Landpattern):
    A = {
        0: RectSmdPad().at((-3.4, -2)),
        1: RectSmdPad().at((3.4, -2)),
    }
    B = {
        0: RectSmdPad().at((-3.4, 2)),
        1: RectSmdPad().at((3.4, 2)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-3.3, 3), (3.3, 3)])),
        Silkscreen(Polyline(0.127, [(-3.3, -3), (-3.3, 3)])),
        Silkscreen(Polyline(0.127, [(3.3, 3), (3.3, -3)])),
        Silkscreen(Polyline(0.127, [(3.3, -3), (-3.3, -3)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((0, 0), 1, 0, 360)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((0, 0), 1.5033, 0, 360)])),
    ]

    models = [
        Model3D("EVQQ2-BFKPUY-03W.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(-90, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_SPST_2_4PIN(Symbol):
    pin_name_size = 0
    pad_name_size = 1.2
    P = Pin((0, -2), 2, Direction.Down)
    P1 = Pin((2, -2), 2, Direction.Down)
    S = Pin((0, 2), 2, Direction.Up)
    S1 = Pin((2, 2), 2, Direction.Up)
    draws = [
        Text(">REF", 1.19, Anchor.W).at(Transform((-5, -2), 90)),
        Text(">VALUE", 1.19, Anchor.W).at(Transform((4.8, -4.8), 90)),
        Text("pcbgolf:EVQ-Q2", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(-3.5, 1.5), (-2.5, 1.5)]),
        Polyline(0.1524, [(2, 2), (0, 2)]),
        Polyline(0.254, [(0, -2), (-1, 1.5)]),
        Polyline(0.254, [(0, 1.5), (0, 2)]),
        Circle(radius=0.1).at(0, 2),
        Polyline(0.1524, [(-1, 0), (-0.5, 0)]),
        Polyline(0.1524, [(-2, 0), (-1.5, 0)]),
        Polyline(0.1524, [(2, -2), (0, -2)]),
        Polyline(0.1524, [(-3.5, 0), (-2.5, 0)]),
        Polyline(0.254, [(-3.5, 0), (-3.5, -1.5)]),
        Circle(radius=0.1).at(0, -2),
        Polyline(0.254, [(-3.5, 1.5), (-3.5, 0)]),
        Polyline(0.254, [(-3.5, -1.5), (-2.5, -1.5)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class EVQ_Q2Y03W(Component):
    description = ""
    mpn = "EVQ-Q2Y03W"
    datasheet = ""
    reference_designator_prefix = "SW1"
    landpattern = LandpatternEVQ_Q2()
    P = Port()
    P1 = Port()
    S = Port()
    S1 = Port()
    symbol = Symbolcomma_ai_11112255_SPST_2_4PIN()
    mappings = [
        SymbolMapping({
            P: symbol.P, 
            P1: symbol.P1, 
            S: symbol.S, 
            S1: symbol.S1
        }),
        PadMapping({
            P: landpattern.A[0],
            P1: landpattern.A[1],
            S: landpattern.B[0],
            S1: landpattern.B[1],
        }),
    ]

Device: type[EVQ_Q2Y03W] = EVQ_Q2Y03W
