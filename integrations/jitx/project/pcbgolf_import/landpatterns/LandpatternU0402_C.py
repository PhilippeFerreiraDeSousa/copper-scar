# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/landpatterns/LandpatternU0402_C.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Courtyard, Glue, Soldermask
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
    shape = rectangle(0.6, 0.6)
    paste = [
        Paste(rectangle(0.6, 0.6)),
    ]
    soldermask = [
        Soldermask(rectangle(0.6, 0.6)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0402_C(Landpattern):
    p = {
        1: RectSmdPad().at((-0.45, 0)),
        2: RectSmdPad().at((0.45, 0)),
    }

    customlayer = [
        Custom(Polyline(0.1524, [(-0.245, 0.224), (0.245, 0.224)]), name="Fab"),
        Custom(Polyline(0.1524, [(0.245, -0.224), (-0.245, -0.224)]), name="Fab"),
        Custom(Polygon([
            (-0.554, -0.3048),
            (-0.254, -0.3048),
            (-0.254, 0.2951),
            (-0.554, 0.2951)]), name="Fab"),
        Custom(Polygon([
            (0.2588, -0.3048),
            (0.5588, -0.3048),
            (0.5588, 0.2951),
            (0.2588, 0.2951)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(-0.9, 0.45), (-0.9, -0.45)])),
        Silkscreen(Polyline(0.127, [(-0.9, -0.45), (0.9, -0.45)])),
        Silkscreen(Polyline(0.127, [(0.9, 0.45), (-0.9, 0.45)])),
        Silkscreen(Polyline(0.127, [(0.9, -0.45), (0.9, 0.45)])),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-0.973, 0.483),
            (0.973, 0.483),
            (0.973, -0.483),
            (-0.973, -0.483)])),
    ]
    glue = [
        Glue(Polygon([
            (-0.1999, -0.4001),
            (0.1999, -0.4001),
            (0.1999, 0.4001),
            (-0.1999, 0.4001)])),
    ]

    models = [
        Model3D("C_0402_1005Metric.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

