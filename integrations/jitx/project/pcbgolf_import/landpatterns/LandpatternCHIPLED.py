# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/landpatterns/LandpatternCHIPLED.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
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

    models = [
        Model3D("LED_0805_2012Metric.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 90),
        ),
    ]

