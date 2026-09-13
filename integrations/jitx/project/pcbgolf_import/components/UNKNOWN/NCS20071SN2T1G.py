# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/NCS20071SN2T1G.py 
# To import this component:
#     from .components.UNKNOWN import NCS20071SN2T1G
#     u1 = NCS20071SN2T1G.NCS20071SN2T1G()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Soldermask, Courtyard
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Polygon, Text
from jitx.shapes.composites import rectangle
from jitx.transform import Transform


class RoundRectSmdPad(Pad):
    shape = rectangle(1.95, 0.6, radius=0.15)
    paste = [
        Paste(rectangle(1.95, 0.6, radius=0.15)),
    ]
    soldermask = [
        Soldermask(rectangle(1.95, 0.6, radius=0.15)),
    ]

class LandpatternSOIC_8_3_9x4_9mm_P1_27mm_1(Landpattern):
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
        Custom(Text(">REF", 1, Anchor.C).at(Transform((0, 0), 90)), name="Fab"),
        Custom(Polyline(0.1, [(-0.975, 2.45), (1.95, 2.45), (1.95, -2.45), (-1.95, -2.45), (-1.95, 1.475), (-0.975, 2.45)]), name="Fab"),
    ]
    if False : # hidden objects
        hidden = Text(">VALUE", 1, Anchor.C).at((0, 3.4))
    silkscreen = [
        Silkscreen(Polyline(0.12, [(-2.06, 2.56), (2.06, 2.56)])),
        Silkscreen(Polyline(0.12, [(-2.06, 2.465), (-2.06, 2.56)])),
        Silkscreen(Polyline(0.12, [(-2.06, -2.56), (-2.06, -2.465)])),
        Silkscreen(Polyline(0.12, [(2.06, 2.56), (2.06, 2.465)])),
        Silkscreen(Polyline(0.12, [(2.06, -2.465), (2.06, -2.56)])),
        Silkscreen(Polyline(0.12, [(2.06, -2.56), (-2.06, -2.56)])),
        Silkscreen(Polygon([
            (-2.6, 2.47),
            (-2.84, 2.8),
            (-2.36, 2.8)])),
    ]
    if False : # hidden objects
        hidden = Text(">REF", 1, Anchor.C).at((0, -3.4))
    courtyard = [
        Courtyard(Polygon([
            (-3.7, 2.46),
            (-2.2, 2.46),
            (-2.2, 2.7),
            (2.2, 2.7),
            (2.2, 2.46),
            (3.7, 2.46),
            (3.7, -2.46),
            (2.2, -2.46),
            (2.2, -2.7),
            (-2.2, -2.7),
            (-2.2, -2.46),
            (-3.7, -2.46)])),
    ]

    models = [
        Model3D("SOIC-8_3.9x4.9mm_P1.27mm.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class SymbolNCS20071XV(Symbol):
    pin_name_size = 1
    pad_name_size = 1
    p = {
        0: Pin((-4, 2), 2, Direction.Left),
        1: Pin((4, 0), 2, Direction.Right),
    }
    Vn = Pin((-2, -3), 3, Direction.Down)
    n = Pin((-4, -2), 2, Direction.Left)
    Vp = Pin((-2, 3), 3, Direction.Up)
    draw = Polygon([
        (4, 0),
        (-4, 4),
        (-4, -4),
        (4, 0)])

class NCS20071SN2T1G(Component):
    description = "Single, 2.8V/µs, Rail-to-Rail Output, SOT-553"
    mpn = "NCS20071SN2T1G"
    datasheet = "https://www.onsemi.com/pub/Collateral/NCS20071-D.PDF"
    reference_designator_prefix = "U"
    landpattern = LandpatternSOIC_8_3_9x4_9mm_P1_27mm_1()
    p = {
        0: Port(),
        1: Port(),
    }
    Vn = Port()
    n = Port()
    Vp = Port()
    symbol = SymbolNCS20071XV()
    mappings = [
        SymbolMapping({
            p[0]: symbol.p[0], 
            Vn: symbol.Vn, 
            n: symbol.n, 
            p[1]: symbol.p[1], 
            Vp: symbol.Vp
        }),
        PadMapping({
            p[0]: landpattern.p[1],
            Vn: landpattern.p[2],
            n: landpattern.p[3],
            p[1]: landpattern.p[4],
            Vp: landpattern.p[5],
        }),
    ]

Device: type[NCS20071SN2T1G] = NCS20071SN2T1G
