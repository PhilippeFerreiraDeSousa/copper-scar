# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/landpatterns/LandpatternU0805_C.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
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


class RectSmdPad(Pad):
    shape = rectangle(0.8, 1.2)
    paste = [
        Paste(rectangle(0.8, 1.2)),
    ]
    soldermask = [
        Soldermask(rectangle(0.8, 1.2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0805_C(Landpattern):
    p = {
        1: RectSmdPad().at((-0.9, 0)),
        2: RectSmdPad().at((0.9, 0)),
    }

    customlayer = [
        Custom(Polygon([
            (0.508, -0.635),
            (1.016, -0.635),
            (1.016, 0.635),
            (0.508, 0.635)]), name="Fab"),
        Custom(Polygon([
            (-0.508, 0.635),
            (-1.016, 0.635),
            (-1.016, -0.635),
            (-0.508, -0.635)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.5, -0.8), (1.5, 0.8)])),
        Silkscreen(Polyline(0.127, [(1.5, 0.8), (-1.5, 0.8)])),
        Silkscreen(Polyline(0.127, [(-1.5, -0.8), (1.5, -0.8)])),
        Silkscreen(Polyline(0.127, [(-1.5, 0.8), (-1.5, -0.8)])),
    ]

    models = [
        Model3D("C_0805_2012Metric.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

