# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternDX07S024XJ1R1100.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Cutout, Soldermask
from jitx.layerindex import Side
from jitx.shapes.primitive import Polyline, Circle
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


class CircleThPad_1(Pad):
    shape = Circle(radius=0.3)
    cutout = [
        Cutout(Circle(radius=0.2)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.3)),
        Soldermask(Circle(radius=0.3), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class CircleThPad_2(Pad):
    shape = Circle(radius=0.55)
    cutout = [
        Cutout(Circle(radius=0.3)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.55)),
        Soldermask(Circle(radius=0.55), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class RoundRectSmdPad_1(Pad):
    shape = rectangle(0.3, 1, radius=0.1125)
    paste = [
        Paste(rectangle(0.3, 1, radius=0.1125)),
    ]
    soldermask = [
        Soldermask(rectangle(0.3, 1, radius=0.1125)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RoundRectSmdPad_2(Pad):
    shape = rectangle(0.6096, 0.6096, radius=0.3048)
    paste = [
        Paste(rectangle(0.6096, 0.6096, radius=0.3048)),
    ]
    soldermask = [
        Soldermask(rectangle(0.6096, 0.6096, radius=0.3048)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RoundRectSmdPad_3(Pad):
    shape = rectangle(1.1, 1.9, radius=0.55)
    paste = [
        Paste(rectangle(1.1, 1.9, radius=0.55)),
    ]
    soldermask = [
        Soldermask(rectangle(1.1, 1.9, radius=0.55)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternDX07S024XJ1R1100(Landpattern):
    A1 = RoundRectSmdPad_1().at((-2.75, 0.61))
    A10 = RoundRectSmdPad_1().at((1.75, 0.61))
    A11 = RoundRectSmdPad_1().at((2.25, 0.61))
    A12 = RoundRectSmdPad_1().at((2.75, 0.61))
    A2 = RoundRectSmdPad_1().at((-2.25, 0.61))
    A3 = RoundRectSmdPad_1().at((-1.75, 0.61))
    A4 = RoundRectSmdPad_1().at((-1.25, 0.61))
    A5 = RoundRectSmdPad_1().at((-0.75, 0.61))
    A6 = RoundRectSmdPad_1().at((-0.25, 0.61))
    A7 = RoundRectSmdPad_1().at((0.25, 0.61))
    A8 = RoundRectSmdPad_1().at((0.75, 0.61))
    A9 = RoundRectSmdPad_1().at((1.25, 0.61))
    B1 = CircleThPad_1().at((2.8, -0.65))
    B10 = CircleThPad_1().at((-1.6, -1.35))
    B10T = RoundRectSmdPad_2().at((-1.59951, -1.3485))
    B11 = CircleThPad_1().at((-2.4, -1.35))
    B11T = RoundRectSmdPad_2().at((-2.3975, -1.35049))
    B12 = CircleThPad_1().at((-2.8, -0.65))
    B12T = RoundRectSmdPad_2().at((-2.80069, -0.65116))
    B1T = RoundRectSmdPad_2().at((2.80337, -0.6498))
    B2 = CircleThPad_1().at((2.4, -1.35))
    B2T = RoundRectSmdPad_2().at((2.39846, -1.35365))
    B3 = CircleThPad_1().at((1.6, -1.35))
    B3T = RoundRectSmdPad_2().at((1.60274, -1.34977))
    B4 = CircleThPad_1().at((1.2, -0.65))
    B4T = RoundRectSmdPad_2().at((1.20082, -0.65074))
    B5 = CircleThPad_1().at((0.8, -1.35))
    B5T = RoundRectSmdPad_2().at((0.79673, -1.34897))
    B6 = CircleThPad_1().at((0.4, -0.65))
    B6T = RoundRectSmdPad_2().at((0.40479, -0.65117))
    B7 = CircleThPad_1().at((-0.4, -0.65))
    B7T = RoundRectSmdPad_2().at((-0.40063, -0.64729))
    B8 = CircleThPad_1().at((-0.8, -1.35))
    B8T = RoundRectSmdPad_2().at((-0.79994, -1.3485))
    B9 = CircleThPad_1().at((-1.2, -0.65))
    B9T = RoundRectSmdPad_2().at((-1.20022, -0.65305))
    S1B = RoundRectSmdPad_3().at((-4.6, -1.4), on=Side.Bottom)
    S1T = RoundRectSmdPad_3().at((-4.6, -1.4))
    S1TH = CircleThPad_2().at((-4.6, -1.4))
    S2B = RoundRectSmdPad_3().at((-4.6, -4.4), on=Side.Bottom)
    S2T = RoundRectSmdPad_3().at((-4.6, -4.4))
    S2TH = CircleThPad_2().at((-4.6, -4.4))
    S3B = RoundRectSmdPad_3().at((4.6, -4.4), on=Side.Bottom)
    S3T = RoundRectSmdPad_3().at((4.6, -4.4))
    S3TH = CircleThPad_2().at((4.6, -4.4))
    S4B = RoundRectSmdPad_3().at((4.6, -1.4), on=Side.Bottom)
    S4T = RoundRectSmdPad_3().at((4.6, -1.4))
    S4TH = CircleThPad_2().at((4.6, -1.4))

    customlayer = [
        Custom(Polyline(0.1524, [(-4.695, -8.85), (4.695, -8.85)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-4.6, 1), (-4, 1)])),
        Silkscreen(Polyline(0.1524, [(-4.6, 0), (-4.6, 1)])),
        Silkscreen(Polyline(0.1524, [(4.6, 1), (4, 1)])),
        Silkscreen(Polyline(0.1524, [(4.6, 0), (4.6, 1)])),
    ]
    cutout = [
        Cutout(Circle(radius=0.375).at(-3.6, 0)),
        Cutout(Circle(radius=0.375).at(3.6, 0)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.375).at(-3.6, 0)),
        Soldermask(Circle(radius=0.375).at(-3.6, 0), side=Side.Bottom),
        Soldermask(Circle(radius=0.375).at(3.6, 0)),
        Soldermask(Circle(radius=0.375).at(3.6, 0), side=Side.Bottom),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Connector_USB.3dshapes/DX07S024XJ1R1100.step"

