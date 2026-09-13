# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/components/UNKNOWN/LG_R971_KN_1.py 
# To import this component:
#     from .components.UNKNOWN import LG_R971_KN_1
#     u1 = LG_R971_KN_1.LG_R971_KN_1()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline, Polygon, Text
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
    shape = rectangle(1.2, 1.2)
    paste = [
        Paste(rectangle(1.2, 1.2)),
    ]
    soldermask = [
        Soldermask(rectangle(1.2, 1.2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternCHIPLED(Landpattern):
    A = RectSmdPad().at((0, -1.05))
    C = RectSmdPad().at((0, 1.05))

    customlayer = [
        Custom(Polyline(0.1016, [(0.575, 0.525), (0.575, -0.525)]), name="Fab"),
        Custom(Polyline(0.1016, [(-0.575, -0.5), (-0.575, 0.925)]), name="Fab"),
        Custom(ArcPolyline(0.1016, [
            Arc((0, 1), 0.35, 0, -180)]), name="Fab"),
        Custom(ArcPolyline(0.1016, [
            Arc((-0, -1), 0.35, 180, -180)]), name="Fab"),
        Custom(ArcPolyline(0.1016, [
            Arc((-0.45, 0.85), 0.103, 0, 360)]), name="Fab"),
        Custom(Polygon([
            (0.3, -1),
            (0.625, -1),
            (0.625, -0.5),
            (0.3, -0.5)]), name="Fab"),
        Custom(Polygon([
            (0.3, 0.5),
            (0.625, 0.5),
            (0.625, 1),
            (0.3, 1)]), name="Fab"),
        Custom(Polygon([
            (0.175, -0.75),
            (0.325, -0.75),
            (0.325, -0.5),
            (0.175, -0.5)]), name="Fab"),
        Custom(Polygon([
            (0.175, 0.5),
            (0.325, 0.5),
            (0.325, 0.75),
            (0.175, 0.75)]), name="Fab"),
        Custom(Polygon([
            (-0.2, 0.5),
            (0.2, 0.5),
            (0.2, 0.675),
            (-0.2, 0.675)]), name="Fab"),
        Custom(Polygon([
            (-0.325, -0.75),
            (-0.175, -0.75),
            (-0.175, -0.5),
            (-0.325, -0.5)]), name="Fab"),
        Custom(Polygon([
            (-0.325, 0.5),
            (-0.175, 0.5),
            (-0.175, 0.75),
            (-0.325, 0.75)]), name="Fab"),
        Custom(Polygon([
            (-0.6, 0.5),
            (-0.3, 0.5),
            (-0.3, 0.8),
            (-0.6, 0.8)]), name="Fab"),
        Custom(Polygon([
            (-0.625, -1),
            (-0.3, -1),
            (-0.3, -0.5),
            (-0.625, -0.5)]), name="Fab"),
        Custom(Polygon([
            (-0.625, 0.925),
            (-0.4, 0.925),
            (-0.4, 1),
            (-0.625, 1)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(0.7, -1.8), (0.7, 1.8)])),
        Silkscreen(Polyline(0.127, [(0.7, 1.8), (-0.7, 1.8)])),
        Silkscreen(Polyline(0.127, [(-0.7, -1.8), (0.7, -1.8)])),
        Silkscreen(Polyline(0.127, [(-0.7, 1.8), (-0.7, -1.8)])),
        Silkscreen(Text("+", 0.74778, Anchor.C).at((1.016, -1.778))),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/LED_SMD.3dshapes/LED_0805_2012Metric.step"

class Symbolcomma_ai_11112255_LED_0805(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    A = Pin((0, 0), 2, Direction.Up)
    C = Pin((0, -2), 2, Direction.Down)
    draws = [
        Text(">REF", 1.19, Anchor.W).at((0, 6.29921)),
        Text(">VALUE", 1.19, Anchor.E).at((0, 4.72441)),
        Text("pcbgolf:CHIPLED", 1, Anchor.C).at((0, 3.14961)),
        Text("", 1, Anchor.C).at((0, 1.5748)),
        Polyline(0.254, [(1, 0), (-1, 0)]),
        Polyline(0.254, [(1, 0), (0, -2)]),
        Polyline(0.254, [(0, -2), (-1, -2)]),
        Polyline(0.254, [(0, -2), (-1, 0)]),
        Polyline(0.1524, [(-1.5, -1.5), (-2.6, -2.6)]),
        Polyline(0.1524, [(-1.6, -0.6), (-2.7, -1.7)]),
        Polygon([
            (-2.7, -1.7),
            (-2.4, -1),
            (-2, -1.4),
            (-2.7, -1.7)]),
        Polygon([
            (-2.6, -2.6),
            (-2.3, -1.9),
            (-1.9, -2.3),
            (-2.6, -2.6)]),
        Polyline(0.254, [(1, -2), (0, -2)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class LG_R971_KN_1(Component):
    description = ""
    mpn = "LG R971-KN-1"
    datasheet = ""
    reference_designator_prefix = "LED6"
    landpattern = LandpatternCHIPLED()
    A = Port()
    C = Port()
    symbol = Symbolcomma_ai_11112255_LED_0805()
    mappings = [
        SymbolMapping({
            A: symbol.A, 
            C: symbol.C
        }),
        PadMapping({
            A: landpattern.A,
            C: landpattern.C,
        }),
    ]

Device: type[LG_R971_KN_1] = LG_R971_KN_1
