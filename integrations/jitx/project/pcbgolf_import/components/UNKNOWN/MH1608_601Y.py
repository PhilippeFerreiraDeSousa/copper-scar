# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/MH1608_601Y.py 
# To import this component:
#     from .components.UNKNOWN import MH1608_601Y
#     u1 = MH1608_601Y.MH1608_601Y()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Courtyard, Glue, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline, Polygon, Text
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
    shape = rectangle(1, 1.1)
    paste = [
        Paste(rectangle(1, 1.1)),
    ]
    soldermask = [
        Soldermask(rectangle(1, 1.1)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0603_L(Landpattern):
    p = {
        1: RectSmdPad().at((-0.85, 0)),
        2: RectSmdPad().at((0.85, 0)),
    }

    customlayer = [
        Custom(Polyline(0.1524, [(0.432, 0.356), (-0.432, 0.356)]), name="Fab"),
        Custom(Polyline(0.1524, [(-0.432, -0.356), (0.432, -0.356)]), name="Fab"),
        Custom(Polygon([
            (0.4318, -0.4318),
            (0.8382, -0.4318),
            (0.8382, 0.4318),
            (0.4318, 0.4318)]), name="Fab"),
        Custom(Polygon([
            (-0.8382, -0.4318),
            (-0.4318, -0.4318),
            (-0.4318, 0.4318),
            (-0.8382, 0.4318)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.55, -0.75), (1.55, 0.75)])),
        Silkscreen(Polyline(0.127, [(1.55, 0.75), (-1.55, 0.75)])),
        Silkscreen(Polyline(0.127, [(-1.55, -0.75), (1.55, -0.75)])),
        Silkscreen(Polyline(0.127, [(-1.55, 0.75), (-1.55, -0.75)])),
    ]
    courtyard = [
        Courtyard(Polygon([
            (1.473, -0.983),
            (-1.473, -0.983),
            (-1.473, 0.983),
            (1.473, 0.983)])),
    ]
    glue = [
        Glue(Polygon([
            (-0.1999, -0.4001),
            (0.1999, -0.4001),
            (0.1999, 0.4001),
            (-0.1999, 0.4001)])),
    ]

    models = [
        Model3D("L_0603_1608Metric.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_L_US_L2(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((0, 4), 2, Direction.Up),
        2: Pin((0, -4), 2, Direction.Down),
    }
    draws = [
        Text(">REF", 1.19, Anchor.E).at((-2, 4.4)),
        Text(">VALUE", 1.19, Anchor.W).at((3, -4)),
        Text("pcbgolf:0603-L", 1, Anchor.C).at(Transform((0, 0), 270)),
        Text("", 1, Anchor.C).at(Transform((0, 0), 270)),
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
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class MH1608_601Y(Component):
    description = ""
    mpn = "MH1608-601Y"
    datasheet = ""
    reference_designator_prefix = "L3"
    landpattern = LandpatternU0603_L()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_L_US_L2()
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

Device: type[MH1608_601Y] = MH1608_601Y
