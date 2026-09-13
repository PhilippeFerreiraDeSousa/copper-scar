# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternPP_1212_8.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.shapes.primitive import Polyline
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
    shape = rectangle(0.99, 0.405)
    paste = [
        Paste(rectangle(0.99, 0.405)),
    ]
    soldermask = [
        Soldermask(rectangle(0.99, 0.405)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(0.76, 0.405)
    paste = [
        Paste(rectangle(0.76, 0.405)),
    ]
    soldermask = [
        Soldermask(rectangle(0.76, 0.405)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_3(Pad):
    shape = rectangle(1.725, 2.235)
    paste = [
        Paste(rectangle(1.725, 2.235)),
    ]
    soldermask = [
        Soldermask(rectangle(1.725, 2.235)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternPP_1212_8(Landpattern):
    p = {
        1: RectSmdPad_1().at((-1.4925, 0.99)),
        2: RectSmdPad_1().at((-1.4925, 0.33)),
        3: RectSmdPad_1().at((-1.4925, -0.33)),
        4: RectSmdPad_1().at((-1.4925, -0.99)),
        5: RectSmdPad_2().at((1.4925, -0.99)),
        6: RectSmdPad_2().at((1.4925, -0.33)),
        7: RectSmdPad_2().at((1.4925, 0.33)),
        8: RectSmdPad_2().at((1.4925, 0.99)),
        9: RectSmdPad_3().at((0.5, 0)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-1.65, 1.65), (1.65, 1.65)])),
        Silkscreen(Polyline(0.1524, [(-1.65, -1.65), (1.65, -1.65)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_DFN_QFN.3dshapes/SI7101DN-T1-GE3.step"

