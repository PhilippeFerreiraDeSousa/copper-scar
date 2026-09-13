# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternDCJACK_2MM_SMT.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Cutout, Soldermask
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

def make_pastemask (
    pad_shape,
    *,
    amount: float | None = None,
    thruhole: bool = False):
    return make_mask_expansion(pad_shape, Paste, amount, thruhole)


class RectSmdPad(Pad):
    shape = rectangle(2.4, 2)
    paste = [
        Paste(rectangle(2.4, 2)),
    ]
    soldermask = [
        Soldermask(rectangle(2.4, 2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternDCJACK_2MM_SMT(Landpattern):
    GND = RectSmdPad().at((0, -5.5))
    GNDBREAK = RectSmdPad().at((6.2, -5.5))
    PWR1 = RectSmdPad().at((0, 5.5))
    PWR2 = RectSmdPad().at((6.2, 5.5))

    customlayer = [
        Custom(Polyline(0.127, [(-5, 3.5), (-5, -3.5)]), name="Fab"),
        Custom(Polyline(0.127, [(-4, -4.5), (10.254, -4.5)]), name="Fab"),
        Custom(Polyline(0.127, [(9, 4.5), (-4, 4.5)]), name="Fab"),
        Custom(Polyline(0.127, [(9, -1.492), (9, 4.5)]), name="Fab"),
        Custom(Polyline(0.127, [(10.254, -1.492), (9, -1.492)]), name="Fab"),
        Custom(Polyline(0.127, [(10.254, -4.5), (10.254, -1.492)]), name="Fab"),
        Custom(ArcPolyline(0.127, [
            Arc((-4, 3.5), 1, 180.00004, -90.00009)]), name="Fab"),
        Custom(ArcPolyline(0.127, [
            Arc((-4, -3.5), 1, 270.00004, -90.00009)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(-5, 3.5), (-5, -3.5)])),
        Silkscreen(Polyline(0.127, [(-4, -4.5), (-1.684, -4.5)])),
        Silkscreen(Polyline(0.127, [(-1.668, 4.5), (-4, 4.5)])),
        Silkscreen(Polyline(0.127, [(1.588, -4.5), (4.666, -4.5)])),
        Silkscreen(Polyline(0.127, [(4.682, 4.5), (1.588, 4.5)])),
        Silkscreen(Polyline(0.127, [(7.938, -4.5), (10.254, -4.5)])),
        Silkscreen(Polyline(0.127, [(9, 4.5), (7.938, 4.5)])),
        Silkscreen(Polyline(0.127, [(9, -1.492), (9, 4.5)])),
        Silkscreen(Polyline(0.127, [(10.254, -1.492), (9, -1.492)])),
        Silkscreen(Polyline(0.127, [(10.254, -4.5), (10.254, -1.492)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-4, 3.5), 1, 180.00004, -90.00009)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-4, -3.5), 1, 270.00004, -90.00009)])),
        Silkscreen(Text("GND", 0.74778, Anchor.C).at((-1.016, -3.81))),
        Silkscreen(Text("+", 1.25171, Anchor.C).at(Transform((0.762, 2.794), 90))),
    ]
    cutout = [
        Cutout(Circle(radius=0.8)),
        Cutout(Circle(radius=0.9).at(4.5, 0)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.8)),
        Soldermask(Circle(radius=0.8), side=Side.Bottom),
        Soldermask(Circle(radius=0.9).at(4.5, 0)),
        Soldermask(Circle(radius=0.9).at(4.5, 0), side=Side.Bottom),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Connector_BarrelJack.3dshapes/PJ-002AH-SMT-TR.step"

