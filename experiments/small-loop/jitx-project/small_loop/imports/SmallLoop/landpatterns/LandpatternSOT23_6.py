# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternSOT23_6.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
from jitx.shapes.primitive import Polyline, Circle, Polygon
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
    shape = rectangle(0.6, 0.9)
    paste = [
        Paste(rectangle(0.6, 0.9)),
    ]
    soldermask = [
        Soldermask(rectangle(0.6, 0.9)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternSOT23_6(Landpattern):
    p = {
        1: RectSmdPad().at((-0.95, -1.15)),
        2: RectSmdPad().at((0, -1.15)),
        3: RectSmdPad().at((0.95, -1.15)),
        4: RectSmdPad().at((0.95, 1.15)),
        5: RectSmdPad().at((0, 1.15)),
        6: RectSmdPad().at((-0.95, 1.15)),
    }

    customlayer = [
        Custom(Polyline(0.1524, [(-1.423, 0.781), (1.422, 0.781)]), name="Fab"),
        Custom(Polyline(0.1524, [(1.422, -0.781), (-1.423, -0.781)]), name="Fab"),
        Custom(Polygon([
            (0.7, 0.8),
            (1.2, 0.8),
            (1.2, 1.4),
            (0.7, 1.4)]), name="Fab"),
        Custom(Polygon([
            (-0.25, 0.8),
            (0.25, 0.8),
            (0.25, 1.4),
            (-0.25, 1.4)]), name="Fab"),
        Custom(Polygon([
            (-1.2, 0.8),
            (-0.7, 0.8),
            (-0.7, 1.4),
            (-1.2, 1.4)]), name="Fab"),
        Custom(Polygon([
            (0.7, -1.4),
            (1.2, -1.4),
            (1.2, -0.8),
            (0.7, -0.8)]), name="Fab"),
        Custom(Polygon([
            (-0.25, -1.4),
            (0.25, -1.4),
            (0.25, -0.8),
            (-0.25, -0.8)]), name="Fab"),
        Custom(Polygon([
            (-1.2, -1.4),
            (-0.7, -1.4),
            (-0.7, -0.8),
            (-1.2, -0.8)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.1524, [(1.422, 0.781), (1.422, -0.781)])),
        Silkscreen(Polyline(0.1524, [(-1.423, -0.781), (-1.423, 0.781)])),
        Silkscreen(Circle(radius=0.05).at(-1.15, -0.5)),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_TO_SOT_SMD.3dshapes/SOT-23-6.step"

