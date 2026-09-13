# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternUSB_C_FEMALE_VERT_GCT.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Custom, Paste, Cutout, Soldermask, Courtyard
from jitx.layerindex import Side
from jitx.shapes.primitive import Polyline, Circle, Polygon
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


class CircleThPad(Pad):
    shape = Circle(radius=0.55)
    cutout = [
        Cutout(Circle(radius=0.35)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.55)),
        Soldermask(Circle(radius=0.55), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class RectSmdPad_1(Pad):
    shape = rectangle(0.3, 0.88)
    paste = [
        Paste(rectangle(0.3, 0.88)),
    ]
    soldermask = [
        Soldermask(rectangle(0.3, 0.88)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.03, 0.5)
    paste = [
        Paste(rectangle(1.03, 0.5)),
    ]
    soldermask = [
        Soldermask(rectangle(1.03, 0.5)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternUSB_C_FEMALE_VERT_GCT(Landpattern):
    A1 = RectSmdPad_1().at((-2.75, 0.83))
    A10 = RectSmdPad_1().at((1.75, 0.83))
    A11 = RectSmdPad_1().at((2.25, 0.83))
    A12 = RectSmdPad_1().at((2.75, 0.83))
    A2 = RectSmdPad_1().at((-2.25, 0.83))
    A3 = RectSmdPad_1().at((-1.75, 0.83))
    A4 = RectSmdPad_1().at((-1.25, 0.83))
    A5 = RectSmdPad_1().at((-0.75, 0.83))
    A6 = RectSmdPad_1().at((-0.25, 0.83))
    A7 = RectSmdPad_1().at((0.25, 0.83))
    A8 = RectSmdPad_1().at((0.75, 0.83))
    A9 = RectSmdPad_1().at((1.25, 0.83))
    B1 = RectSmdPad_1().at((2.75, -0.83))
    B10 = RectSmdPad_1().at((-1.75, -0.83))
    B11 = RectSmdPad_1().at((-2.25, -0.83))
    B12 = RectSmdPad_1().at((-2.75, -0.83))
    B2 = RectSmdPad_1().at((2.25, -0.83))
    B3 = RectSmdPad_1().at((1.75, -0.83))
    B4 = RectSmdPad_1().at((1.25, -0.83))
    B5 = RectSmdPad_1().at((0.75, -0.83))
    B6 = RectSmdPad_1().at((0.25, -0.83))
    B7 = RectSmdPad_1().at((-0.25, -0.83))
    B8 = RectSmdPad_1().at((-0.75, -0.83))
    B9 = RectSmdPad_1().at((-1.25, -0.83))
    S1 = CircleThPad().at((-2.4, 2.15))
    S11 = RectSmdPad_2().at(Transform((-3.75, 1), 39))
    S12 = RectSmdPad_2().at(Transform((3.75, 1), 321))
    S13 = RectSmdPad_2().at(Transform((3.75, -1), 39))
    S14 = RectSmdPad_2().at(Transform((-3.75, -1), 321))
    S2 = CircleThPad().at((2.4, 2.15))
    S3 = CircleThPad().at((2.4, -2.15))
    S4 = CircleThPad().at((-2.4, -2.15))

    customlayer = [
        Custom(Polyline(0.1524, [(-4.25, 1.35), (4.25, 1.35)]), name="Fab"),
        Custom(Polyline(0.1524, [(-4.25, -1.35), (-4.25, 1.35)]), name="Fab"),
        Custom(Polyline(0.1524, [(4.25, 1.35), (4.25, -1.35)]), name="Fab"),
        Custom(Polyline(0.1524, [(4.25, -1.35), (-4.25, -1.35)]), name="Fab"),
    ]
    cutout = [
        Cutout(Circle(radius=0.33).at(-3.75, 0)),
        Cutout(Circle(radius=0.33).at(3.75, 0)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.33).at(-3.75, 0)),
        Soldermask(Circle(radius=0.33).at(-3.75, 0), side=Side.Bottom),
        Soldermask(Circle(radius=0.33).at(3.75, 0)),
        Soldermask(Circle(radius=0.33).at(3.75, 0), side=Side.Bottom),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-0.8, 1.8),
            (0.8, 1.8),
            (0.8, 2.5),
            (-0.8, 2.5)])),
        Courtyard(Polygon([
            (-0.8, -2.5),
            (0.8, -2.5),
            (0.8, -1.8),
            (-0.8, -1.8)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Connector_USB.3dshapes/10132328-10011LF.step"

