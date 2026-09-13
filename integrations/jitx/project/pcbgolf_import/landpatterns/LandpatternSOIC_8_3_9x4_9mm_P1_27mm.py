# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/landpatterns/LandpatternSOIC_8_3_9x4_9mm_P1_27mm.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Soldermask, Courtyard
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Polygon, Text
from jitx.shapes.composites import rectangle


class RoundRectSmdPad(Pad):
    shape = rectangle(1.95, 0.6, radius=0.15)
    paste = [
        Paste(rectangle(1.95, 0.6, radius=0.15)),
    ]
    soldermask = [
        Soldermask(rectangle(1.95, 0.6, radius=0.15)),
    ]

class LandpatternSOIC_8_3_9x4_9mm_P1_27mm(Landpattern):
    p = {
        1: RoundRectSmdPad().at((-2.475, 1.905)),
        2: RoundRectSmdPad().at((-2.475, 0.635)),
        3: RoundRectSmdPad().at((-2.475, -0.635)),
        4: RoundRectSmdPad().at((-2.475, -1.905)),
        5: RoundRectSmdPad().at((2.475, -1.905)),
        6: RoundRectSmdPad().at((2.475, -0.635)),
        7: RoundRectSmdPad().at((2.475, 0.635)),
        8: RoundRectSmdPad().at((2.475, 1.905)),
    }

    customlayer = [
        Custom(Polyline(0.1, [(-1.95, 1.475), (-0.975, 2.45)]), name="Fab"),
        Custom(Polyline(0.1, [(-1.95, -2.45), (-1.95, 1.475)]), name="Fab"),
        Custom(Polyline(0.1, [(-0.975, 2.45), (1.95, 2.45)]), name="Fab"),
        Custom(Polyline(0.1, [(1.95, 2.45), (1.95, -2.45)]), name="Fab"),
        Custom(Polyline(0.1, [(1.95, -2.45), (-1.95, -2.45)]), name="Fab"),
        Custom(Text("${REFERENCE}", 0.98, Anchor.C), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.12, [(0, 2.56), (-1.95, 2.56)])),
        Silkscreen(Polyline(0.12, [(0, 2.56), (1.95, 2.56)])),
        Silkscreen(Polyline(0.12, [(0, -2.56), (-1.95, -2.56)])),
        Silkscreen(Polyline(0.12, [(0, -2.56), (1.95, -2.56)])),
        Silkscreen(Polygon([
            (-2.7, 2.465),
            (-2.94, 2.795),
            (-2.46, 2.795),
            (-2.7, 2.465)])),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-3.7, 2.7),
            (-3.7, -2.7),
            (3.7, -2.7),
            (3.7, 2.7)])),
    ]

    models = [
        Model3D("SOIC-8_3.9x4.9mm_P1.27mm.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

