# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternU0472192001.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Paste, Soldermask, Courtyard
from jitx.shapes.primitive import Polyline, Polygon
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
    shape = rectangle(0.7, 1.5)
    paste = [
        Paste(rectangle(0.7, 1.5)),
    ]
    soldermask = [
        Soldermask(rectangle(0.7, 1.5)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.45, 2)
    paste = [
        Paste(rectangle(1.45, 2)),
    ]
    soldermask = [
        Soldermask(rectangle(1.45, 2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0472192001(Landpattern):
    p = {
        1: RectSmdPad_1().at((-3.67, 2.6)),
        2: RectSmdPad_1().at((-4.77, 2.6)),
        3: RectSmdPad_1().at((-5.87, 2.6)),
        4: RectSmdPad_1().at((-6.97, 2.6)),
        5: RectSmdPad_1().at((-8.07, 2.6)),
        6: RectSmdPad_1().at((-9.17, 2.6)),
        7: RectSmdPad_1().at((-10.27, 2.6)),
        8: RectSmdPad_1().at((-11.37, 2.6)),
    }
    G1 = RectSmdPad_2().at((0, 0))
    G2 = RectSmdPad_2().at((0, 8.3))
    G3 = RectSmdPad_2().at((-13.75, 8.3))
    G4 = RectSmdPad_2().at((-13.75, 0))

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-13.7, 11.95), (-13.7, 9.6)])),
        Silkscreen(Polyline(0.127, [(-13.7, 11.95), (-0.05, 11.95)])),
        Silkscreen(Polyline(0.127, [(-13.7, 1.3), (-13.7, 7)])),
        Silkscreen(Polyline(0.127, [(-13.7, -2.55), (-13.7, -1.3)])),
        Silkscreen(Polyline(0.127, [(-13.7, -2.55), (-0.05, -2.55)])),
        Silkscreen(Polyline(0.127, [(-0.05, 11.95), (-0.05, 9.6)])),
        Silkscreen(Polyline(0.127, [(-0.05, 1.3), (-0.05, 7)])),
        Silkscreen(Polyline(0.127, [(-0.05, -2.55), (-0.05, -1.3)])),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-13.7, -2.6),
            (-0.1, -2.6),
            (-0.1, 11.9),
            (-13.7, 11.9)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Connector_Card.3dshapes/472192001.step"

