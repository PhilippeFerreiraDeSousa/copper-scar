# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/STM32H725ZGT.py 
# To import this component:
#     from .components.UNKNOWN import STM32H725ZGT
#     u1 = STM32H725ZGT.STM32H725ZGT()
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


class RoundRectSmdPad_1(Pad):
    shape = rectangle(1.475, 0.3, radius=0.075)
    paste = [
        Paste(rectangle(1.475, 0.3, radius=0.075)),
    ]
    soldermask = [
        Soldermask(rectangle(1.475, 0.3, radius=0.075)),
    ]

class RoundRectSmdPad_2(Pad):
    shape = rectangle(0.3, 1.475, radius=0.075)
    paste = [
        Paste(rectangle(0.3, 1.475, radius=0.075)),
    ]
    soldermask = [
        Soldermask(rectangle(0.3, 1.475, radius=0.075)),
    ]

class LandpatternLQFP_144_20x20mm_P0_5mm_1(Landpattern):
    p = {
        1: RoundRectSmdPad_1().at((-10.6625, 8.75)),
        2: RoundRectSmdPad_1().at((-10.6625, 8.25)),
        3: RoundRectSmdPad_1().at((-10.6625, 7.75)),
        4: RoundRectSmdPad_1().at((-10.6625, 7.25)),
        5: RoundRectSmdPad_1().at((-10.6625, 6.75)),
        6: RoundRectSmdPad_1().at((-10.6625, 6.25)),
        7: RoundRectSmdPad_1().at((-10.6625, 5.75)),
        8: RoundRectSmdPad_1().at((-10.6625, 5.25)),
        9: RoundRectSmdPad_1().at((-10.6625, 4.75)),
        10: RoundRectSmdPad_1().at((-10.6625, 4.25)),
        11: RoundRectSmdPad_1().at((-10.6625, 3.75)),
        12: RoundRectSmdPad_1().at((-10.6625, 3.25)),
        13: RoundRectSmdPad_1().at((-10.6625, 2.75)),
        14: RoundRectSmdPad_1().at((-10.6625, 2.25)),
        15: RoundRectSmdPad_1().at((-10.6625, 1.75)),
        16: RoundRectSmdPad_1().at((-10.6625, 1.25)),
        17: RoundRectSmdPad_1().at((-10.6625, 0.75)),
        18: RoundRectSmdPad_1().at((-10.6625, 0.25)),
        19: RoundRectSmdPad_1().at((-10.6625, -0.25)),
        20: RoundRectSmdPad_1().at((-10.6625, -0.75)),
        21: RoundRectSmdPad_1().at((-10.6625, -1.25)),
        22: RoundRectSmdPad_1().at((-10.6625, -1.75)),
        23: RoundRectSmdPad_1().at((-10.6625, -2.25)),
        24: RoundRectSmdPad_1().at((-10.6625, -2.75)),
        25: RoundRectSmdPad_1().at((-10.6625, -3.25)),
        26: RoundRectSmdPad_1().at((-10.6625, -3.75)),
        27: RoundRectSmdPad_1().at((-10.6625, -4.25)),
        28: RoundRectSmdPad_1().at((-10.6625, -4.75)),
        29: RoundRectSmdPad_1().at((-10.6625, -5.25)),
        30: RoundRectSmdPad_1().at((-10.6625, -5.75)),
        31: RoundRectSmdPad_1().at((-10.6625, -6.25)),
        32: RoundRectSmdPad_1().at((-10.6625, -6.75)),
        33: RoundRectSmdPad_1().at((-10.6625, -7.25)),
        34: RoundRectSmdPad_1().at((-10.6625, -7.75)),
        35: RoundRectSmdPad_1().at((-10.6625, -8.25)),
        36: RoundRectSmdPad_1().at((-10.6625, -8.75)),
        37: RoundRectSmdPad_2().at((-8.75, -10.6625)),
        38: RoundRectSmdPad_2().at((-8.25, -10.6625)),
        39: RoundRectSmdPad_2().at((-7.75, -10.6625)),
        40: RoundRectSmdPad_2().at((-7.25, -10.6625)),
        41: RoundRectSmdPad_2().at((-6.75, -10.6625)),
        42: RoundRectSmdPad_2().at((-6.25, -10.6625)),
        43: RoundRectSmdPad_2().at((-5.75, -10.6625)),
        44: RoundRectSmdPad_2().at((-5.25, -10.6625)),
        45: RoundRectSmdPad_2().at((-4.75, -10.6625)),
        46: RoundRectSmdPad_2().at((-4.25, -10.6625)),
        47: RoundRectSmdPad_2().at((-3.75, -10.6625)),
        48: RoundRectSmdPad_2().at((-3.25, -10.6625)),
        49: RoundRectSmdPad_2().at((-2.75, -10.6625)),
        50: RoundRectSmdPad_2().at((-2.25, -10.6625)),
        51: RoundRectSmdPad_2().at((-1.75, -10.6625)),
        52: RoundRectSmdPad_2().at((-1.25, -10.6625)),
        53: RoundRectSmdPad_2().at((-0.75, -10.6625)),
        54: RoundRectSmdPad_2().at((-0.25, -10.6625)),
        55: RoundRectSmdPad_2().at((0.25, -10.6625)),
        56: RoundRectSmdPad_2().at((0.75, -10.6625)),
        57: RoundRectSmdPad_2().at((1.25, -10.6625)),
        58: RoundRectSmdPad_2().at((1.75, -10.6625)),
        59: RoundRectSmdPad_2().at((2.25, -10.6625)),
        60: RoundRectSmdPad_2().at((2.75, -10.6625)),
        61: RoundRectSmdPad_2().at((3.25, -10.6625)),
        62: RoundRectSmdPad_2().at((3.75, -10.6625)),
        63: RoundRectSmdPad_2().at((4.25, -10.6625)),
        64: RoundRectSmdPad_2().at((4.75, -10.6625)),
        65: RoundRectSmdPad_2().at((5.25, -10.6625)),
        66: RoundRectSmdPad_2().at((5.75, -10.6625)),
        67: RoundRectSmdPad_2().at((6.25, -10.6625)),
        68: RoundRectSmdPad_2().at((6.75, -10.6625)),
        69: RoundRectSmdPad_2().at((7.25, -10.6625)),
        70: RoundRectSmdPad_2().at((7.75, -10.6625)),
        71: RoundRectSmdPad_2().at((8.25, -10.6625)),
        72: RoundRectSmdPad_2().at((8.75, -10.6625)),
        73: RoundRectSmdPad_1().at((10.6625, -8.75)),
        74: RoundRectSmdPad_1().at((10.6625, -8.25)),
        75: RoundRectSmdPad_1().at((10.6625, -7.75)),
        76: RoundRectSmdPad_1().at((10.6625, -7.25)),
        77: RoundRectSmdPad_1().at((10.6625, -6.75)),
        78: RoundRectSmdPad_1().at((10.6625, -6.25)),
        79: RoundRectSmdPad_1().at((10.6625, -5.75)),
        80: RoundRectSmdPad_1().at((10.6625, -5.25)),
        81: RoundRectSmdPad_1().at((10.6625, -4.75)),
        82: RoundRectSmdPad_1().at((10.6625, -4.25)),
        83: RoundRectSmdPad_1().at((10.6625, -3.75)),
        84: RoundRectSmdPad_1().at((10.6625, -3.25)),
        85: RoundRectSmdPad_1().at((10.6625, -2.75)),
        86: RoundRectSmdPad_1().at((10.6625, -2.25)),
        87: RoundRectSmdPad_1().at((10.6625, -1.75)),
        88: RoundRectSmdPad_1().at((10.6625, -1.25)),
        89: RoundRectSmdPad_1().at((10.6625, -0.75)),
        90: RoundRectSmdPad_1().at((10.6625, -0.25)),
        91: RoundRectSmdPad_1().at((10.6625, 0.25)),
        92: RoundRectSmdPad_1().at((10.6625, 0.75)),
        93: RoundRectSmdPad_1().at((10.6625, 1.25)),
        94: RoundRectSmdPad_1().at((10.6625, 1.75)),
        95: RoundRectSmdPad_1().at((10.6625, 2.25)),
        96: RoundRectSmdPad_1().at((10.6625, 2.75)),
        97: RoundRectSmdPad_1().at((10.6625, 3.25)),
        98: RoundRectSmdPad_1().at((10.6625, 3.75)),
        99: RoundRectSmdPad_1().at((10.6625, 4.25)),
        100: RoundRectSmdPad_1().at((10.6625, 4.75)),
        101: RoundRectSmdPad_1().at((10.6625, 5.25)),
        102: RoundRectSmdPad_1().at((10.6625, 5.75)),
        103: RoundRectSmdPad_1().at((10.6625, 6.25)),
        104: RoundRectSmdPad_1().at((10.6625, 6.75)),
        105: RoundRectSmdPad_1().at((10.6625, 7.25)),
        106: RoundRectSmdPad_1().at((10.6625, 7.75)),
        107: RoundRectSmdPad_1().at((10.6625, 8.25)),
        108: RoundRectSmdPad_1().at((10.6625, 8.75)),
        109: RoundRectSmdPad_2().at((8.75, 10.6625)),
        110: RoundRectSmdPad_2().at((8.25, 10.6625)),
        111: RoundRectSmdPad_2().at((7.75, 10.6625)),
        112: RoundRectSmdPad_2().at((7.25, 10.6625)),
        113: RoundRectSmdPad_2().at((6.75, 10.6625)),
        114: RoundRectSmdPad_2().at((6.25, 10.6625)),
        115: RoundRectSmdPad_2().at((5.75, 10.6625)),
        116: RoundRectSmdPad_2().at((5.25, 10.6625)),
        117: RoundRectSmdPad_2().at((4.75, 10.6625)),
        118: RoundRectSmdPad_2().at((4.25, 10.6625)),
        119: RoundRectSmdPad_2().at((3.75, 10.6625)),
        120: RoundRectSmdPad_2().at((3.25, 10.6625)),
        121: RoundRectSmdPad_2().at((2.75, 10.6625)),
        122: RoundRectSmdPad_2().at((2.25, 10.6625)),
        123: RoundRectSmdPad_2().at((1.75, 10.6625)),
        124: RoundRectSmdPad_2().at((1.25, 10.6625)),
        125: RoundRectSmdPad_2().at((0.75, 10.6625)),
        126: RoundRectSmdPad_2().at((0.25, 10.6625)),
        127: RoundRectSmdPad_2().at((-0.25, 10.6625)),
        128: RoundRectSmdPad_2().at((-0.75, 10.6625)),
        129: RoundRectSmdPad_2().at((-1.25, 10.6625)),
        130: RoundRectSmdPad_2().at((-1.75, 10.6625)),
        131: RoundRectSmdPad_2().at((-2.25, 10.6625)),
        132: RoundRectSmdPad_2().at((-2.75, 10.6625)),
        133: RoundRectSmdPad_2().at((-3.25, 10.6625)),
        134: RoundRectSmdPad_2().at((-3.75, 10.6625)),
        135: RoundRectSmdPad_2().at((-4.25, 10.6625)),
        136: RoundRectSmdPad_2().at((-4.75, 10.6625)),
        137: RoundRectSmdPad_2().at((-5.25, 10.6625)),
        138: RoundRectSmdPad_2().at((-5.75, 10.6625)),
        139: RoundRectSmdPad_2().at((-6.25, 10.6625)),
        140: RoundRectSmdPad_2().at((-6.75, 10.6625)),
        141: RoundRectSmdPad_2().at((-7.25, 10.6625)),
        142: RoundRectSmdPad_2().at((-7.75, 10.6625)),
        143: RoundRectSmdPad_2().at((-8.25, 10.6625)),
        144: RoundRectSmdPad_2().at((-8.75, 10.6625)),
    }

    customlayer = [
        Custom(Text(">REF", 1, Anchor.C), name="Fab"),
        Custom(Polyline(0.1, [(-9, 10), (10, 10), (10, -10), (-10, -10), (-10, 9), (-9, 10)]), name="Fab"),
    ]
    if False : # hidden objects
        hidden = Text(">VALUE", 1, Anchor.C).at((0, 12.35))
    silkscreen = [
        Silkscreen(Polyline(0.12, [(-10.11, 10.11), (-9.16, 10.11)])),
        Silkscreen(Polyline(0.12, [(-10.11, 9.16), (-10.11, 10.11)])),
        Silkscreen(Polyline(0.12, [(-10.11, -10.11), (-10.11, -9.16)])),
        Silkscreen(Polyline(0.12, [(-9.16, -10.11), (-10.11, -10.11)])),
        Silkscreen(Polyline(0.12, [(9.16, 10.11), (10.11, 10.11)])),
        Silkscreen(Polyline(0.12, [(10.11, 10.11), (10.11, 9.16)])),
        Silkscreen(Polyline(0.12, [(10.11, -9.16), (10.11, -10.11)])),
        Silkscreen(Polyline(0.12, [(10.11, -10.11), (9.16, -10.11)])),
        Silkscreen(Polygon([
            (-10.75, 9.16),
            (-11.09, 9.63),
            (-10.41, 9.63)])),
    ]
    if False : # hidden objects
        hidden = Text(">REF", 1, Anchor.C).at((0, -12.35))
    courtyard = [
        Courtyard(Polygon([
            (-11.65, 9.15),
            (-10.25, 9.15),
            (-10.25, 10.25),
            (-9.15, 10.25),
            (-9.15, 11.65),
            (9.15, 11.65),
            (9.15, 10.25),
            (10.25, 10.25),
            (10.25, 9.15),
            (11.65, 9.15),
            (11.65, -9.15),
            (10.25, -9.15),
            (10.25, -10.25),
            (9.15, -10.25),
            (9.15, -11.65),
            (-9.15, -11.65),
            (-9.15, -10.25),
            (-10.25, -10.25),
            (-10.25, -9.15),
            (-11.65, -9.15)])),
    ]

    models = [
        Model3D("LQFP-144_20x20mm_P0.5mm.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class SymbolSTM32H725ZGTx(Symbol):
    pin_name_size = 1
    pad_name_size = 1
    VDDLDO = {
        0: Pin((14, 70), 4, Direction.Up),
        1: Pin((16, 70), 4, Direction.Up),
        2: Pin((18, 70), 4, Direction.Up),
    }
    VCAP = {
        0: Pin((-34, -32), 4, Direction.Left),
        1: Pin((-34, -34), 4, Direction.Left),
        2: Pin((-34, -36), 4, Direction.Left),
    }
    VDD = {
        0: Pin((-18, 70), 4, Direction.Up),
        1: Pin((-16, 70), 4, Direction.Up),
        2: Pin((-14, 70), 4, Direction.Up),
        3: Pin((-12, 70), 4, Direction.Up),
        4: Pin((-10, 70), 4, Direction.Up),
        5: Pin((-8, 70), 4, Direction.Up),
        6: Pin((-6, 70), 4, Direction.Up),
        7: Pin((-4, 70), 4, Direction.Up),
        8: Pin((-2, 70), 4, Direction.Up),
        9: Pin((0, 70), 4, Direction.Up),
        10: Pin((2, 70), 4, Direction.Up),
        11: Pin((4, 70), 4, Direction.Up),
        12: Pin((6, 70), 4, Direction.Up),
    }
    PE2 = Pin((-34, -2), 4, Direction.Left)
    PE3 = Pin((-34, -4), 4, Direction.Left)
    PE4 = Pin((-34, -6), 4, Direction.Left)
    PE5 = Pin((-34, -8), 4, Direction.Left)
    PE6 = Pin((-34, -10), 4, Direction.Left)
    VBAT = Pin((-20, 70), 4, Direction.Up)
    PC13 = Pin((34, -28), 4, Direction.Right)
    PC14 = Pin((34, -30), 4, Direction.Right)
    PC15 = Pin((34, -32), 4, Direction.Right)
    VSSSMPS = Pin((2, -70), 4, Direction.Down)
    VLXSMPS = Pin((-34, 58), 4, Direction.Left)
    VDDSMPS = Pin((20, 70), 4, Direction.Up)
    VFBSMPS = Pin((-34, 50), 4, Direction.Left)
    PF6 = Pin((-34, 20), 4, Direction.Left)
    PF7 = Pin((-34, 18), 4, Direction.Left)
    PF8 = Pin((-34, 16), 4, Direction.Left)
    PF9 = Pin((-34, 14), 4, Direction.Left)
    PF10 = Pin((-34, 12), 4, Direction.Left)
    PH0 = Pin((-34, 46), 4, Direction.Left)
    PH1 = Pin((-34, 44), 4, Direction.Left)
    NRST = Pin((-34, 66), 4, Direction.Left)
    PC0 = Pin((34, -2), 4, Direction.Right)
    PC1 = Pin((34, -4), 4, Direction.Right)
    PC2_C = Pin((34, -6), 4, Direction.Right)
    PC3_C = Pin((34, -8), 4, Direction.Right)
    VSSA = Pin((0, -70), 4, Direction.Down)
    VREFp = Pin((-34, 56), 4, Direction.Left)
    VDDA = Pin((12, 70), 4, Direction.Up)
    PA0 = Pin((34, 66), 4, Direction.Right)
    PA1 = Pin((34, 64), 4, Direction.Right)
    PA2 = Pin((34, 62), 4, Direction.Right)
    PA3 = Pin((34, 60), 4, Direction.Right)
    PA4 = Pin((34, 58), 4, Direction.Right)
    PA5 = Pin((34, 56), 4, Direction.Right)
    PA6 = Pin((34, 54), 4, Direction.Right)
    PA7 = Pin((34, 52), 4, Direction.Right)
    PC4 = Pin((34, -10), 4, Direction.Right)
    PC5 = Pin((34, -12), 4, Direction.Right)
    PB0 = Pin((34, 32), 4, Direction.Right)
    PB1 = Pin((34, 30), 4, Direction.Right)
    PB2 = Pin((34, 28), 4, Direction.Right)
    PF11 = Pin((-34, 10), 4, Direction.Left)
    PF14 = Pin((-34, 8), 4, Direction.Left)
    PF15 = Pin((-34, 6), 4, Direction.Left)
    PE7 = Pin((-34, -12), 4, Direction.Left)
    PE8 = Pin((-34, -14), 4, Direction.Left)
    PE9 = Pin((-34, -16), 4, Direction.Left)
    PE10 = Pin((-34, -18), 4, Direction.Left)
    PE11 = Pin((-34, -20), 4, Direction.Left)
    PE12 = Pin((-34, -22), 4, Direction.Left)
    PE13 = Pin((-34, -24), 4, Direction.Left)
    PE14 = Pin((-34, -26), 4, Direction.Left)
    PE15 = Pin((-34, -28), 4, Direction.Left)
    PB10 = Pin((34, 12), 4, Direction.Right)
    PB11 = Pin((34, 10), 4, Direction.Right)
    PB12 = Pin((34, 8), 4, Direction.Right)
    PB13 = Pin((34, 6), 4, Direction.Right)
    PB14 = Pin((34, 4), 4, Direction.Right)
    PB15 = Pin((34, 2), 4, Direction.Right)
    PD8 = Pin((34, -52), 4, Direction.Right)
    PD9 = Pin((34, -54), 4, Direction.Right)
    PD10 = Pin((34, -56), 4, Direction.Right)
    PD11 = Pin((34, -58), 4, Direction.Right)
    PD12 = Pin((34, -60), 4, Direction.Right)
    PD13 = Pin((34, -62), 4, Direction.Right)
    PD14 = Pin((34, -64), 4, Direction.Right)
    PD15 = Pin((34, -66), 4, Direction.Right)
    PG6 = Pin((-34, 40), 4, Direction.Left)
    PG7 = Pin((-34, 38), 4, Direction.Left)
    PG8 = Pin((-34, 36), 4, Direction.Left)
    VDD50USB = Pin((10, 70), 4, Direction.Up)
    VDD33USB = Pin((8, 70), 4, Direction.Up)
    PC6 = Pin((34, -14), 4, Direction.Right)
    PC7 = Pin((34, -16), 4, Direction.Right)
    PC8 = Pin((34, -18), 4, Direction.Right)
    PC9 = Pin((34, -20), 4, Direction.Right)
    PA8 = Pin((34, 50), 4, Direction.Right)
    PA9 = Pin((34, 48), 4, Direction.Right)
    PA10 = Pin((34, 46), 4, Direction.Right)
    PA11 = Pin((34, 44), 4, Direction.Right)
    PA12 = Pin((34, 42), 4, Direction.Right)
    PA13JTMS = Pin((34, 40), 4, Direction.Right)
    PA14JTCK = Pin((34, 38), 4, Direction.Right)
    PA15JTDI = Pin((34, 36), 4, Direction.Right)
    PC10 = Pin((34, -22), 4, Direction.Right)
    PC11 = Pin((34, -24), 4, Direction.Right)
    PC12 = Pin((34, -26), 4, Direction.Right)
    PD0 = Pin((34, -36), 4, Direction.Right)
    PD1 = Pin((34, -38), 4, Direction.Right)
    PD2 = Pin((34, -40), 4, Direction.Right)
    PD3 = Pin((34, -42), 4, Direction.Right)
    PD4 = Pin((34, -44), 4, Direction.Right)
    PD5 = Pin((34, -46), 4, Direction.Right)
    PD6 = Pin((34, -48), 4, Direction.Right)
    PD7 = Pin((34, -50), 4, Direction.Right)
    PG9 = Pin((-34, 34), 4, Direction.Left)
    PG10 = Pin((-34, 32), 4, Direction.Left)
    PG11 = Pin((-34, 30), 4, Direction.Left)
    PG12 = Pin((-34, 28), 4, Direction.Left)
    PG13 = Pin((-34, 26), 4, Direction.Left)
    PG14 = Pin((-34, 24), 4, Direction.Left)
    PB3JTDO = Pin((34, 26), 4, Direction.Right)
    PB4NJTRST = Pin((34, 24), 4, Direction.Right)
    PB5 = Pin((34, 22), 4, Direction.Right)
    PB6 = Pin((34, 20), 4, Direction.Right)
    PB7 = Pin((34, 18), 4, Direction.Right)
    BOOT0 = Pin((-34, 62), 4, Direction.Left)
    PB8 = Pin((34, 16), 4, Direction.Right)
    PB9 = Pin((34, 14), 4, Direction.Right)
    PE0 = Pin((-34, 2), 4, Direction.Left)
    PE1 = Pin((-34, 0), 4, Direction.Left)
    VSS = Pin((-2, -70), 4, Direction.Down)
    PDR_ON = Pin((-34, 52), 4, Direction.Left)
    draws = [
        Text(">REF", 1, Anchor.W).at((3.68764, -72)),
        Text(">VALUE", 1, Anchor.W).at((3.68764, -74)),
        Text("pcbgolf:LQFP-144_20x20mm_P0.5mm", 1, Anchor.E).at((-34, -70)),
        Text("https://www.st.com/resource/en/datasheet/stm32h725zg.pdf", 1, Anchor.C),
        rectangle(68, 140),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_keywords: Arm Cortex-M7 STM32H7 STM32H725/735", 1, Anchor.C)

class STM32H725ZGT(Component):
    description = "STMicroelectronics Arm Cortex-M7 MCU, 1024KB flash, 564KB RAM, 550 MHz, 1.62-3.6V, 99 GPIO, LQFP144"
    mpn = "STM32H725ZGT"
    datasheet = "https://www.st.com/resource/en/datasheet/stm32h725zg.pdf"
    reference_designator_prefix = "U3"
    landpattern = LandpatternLQFP_144_20x20mm_P0_5mm_1()
    VDDLDO = {
        0: Port(),
        1: Port(),
        2: Port(),
    }
    VCAP = {
        0: Port(),
        1: Port(),
        2: Port(),
    }
    VDD = {
        0: Port(),
        1: Port(),
        2: Port(),
        3: Port(),
        4: Port(),
        5: Port(),
        6: Port(),
        7: Port(),
        8: Port(),
        9: Port(),
        10: Port(),
        11: Port(),
        12: Port(),
    }
    PE2 = Port()
    PE3 = Port()
    PE4 = Port()
    PE5 = Port()
    PE6 = Port()
    VBAT = Port()
    PC13 = Port()
    PC14 = Port()
    PC15 = Port()
    VSSSMPS = Port()
    VLXSMPS = Port()
    VDDSMPS = Port()
    VFBSMPS = Port()
    PF6 = Port()
    PF7 = Port()
    PF8 = Port()
    PF9 = Port()
    PF10 = Port()
    PH0 = Port()
    PH1 = Port()
    NRST = Port()
    PC0 = Port()
    PC1 = Port()
    PC2_C = Port()
    PC3_C = Port()
    VSSA = Port()
    VREFp = Port()
    VDDA = Port()
    PA0 = Port()
    PA1 = Port()
    PA2 = Port()
    PA3 = Port()
    PA4 = Port()
    PA5 = Port()
    PA6 = Port()
    PA7 = Port()
    PC4 = Port()
    PC5 = Port()
    PB0 = Port()
    PB1 = Port()
    PB2 = Port()
    PF11 = Port()
    PF14 = Port()
    PF15 = Port()
    PE7 = Port()
    PE8 = Port()
    PE9 = Port()
    PE10 = Port()
    PE11 = Port()
    PE12 = Port()
    PE13 = Port()
    PE14 = Port()
    PE15 = Port()
    PB10 = Port()
    PB11 = Port()
    PB12 = Port()
    PB13 = Port()
    PB14 = Port()
    PB15 = Port()
    PD8 = Port()
    PD9 = Port()
    PD10 = Port()
    PD11 = Port()
    PD12 = Port()
    PD13 = Port()
    PD14 = Port()
    PD15 = Port()
    PG6 = Port()
    PG7 = Port()
    PG8 = Port()
    VDD50USB = Port()
    VDD33USB = Port()
    PC6 = Port()
    PC7 = Port()
    PC8 = Port()
    PC9 = Port()
    PA8 = Port()
    PA9 = Port()
    PA10 = Port()
    PA11 = Port()
    PA12 = Port()
    PA13JTMS = Port()
    PA14JTCK = Port()
    PA15JTDI = Port()
    PC10 = Port()
    PC11 = Port()
    PC12 = Port()
    PD0 = Port()
    PD1 = Port()
    PD2 = Port()
    PD3 = Port()
    PD4 = Port()
    PD5 = Port()
    PD6 = Port()
    PD7 = Port()
    PG9 = Port()
    PG10 = Port()
    PG11 = Port()
    PG12 = Port()
    PG13 = Port()
    PG14 = Port()
    PB3JTDO = Port()
    PB4NJTRST = Port()
    PB5 = Port()
    PB6 = Port()
    PB7 = Port()
    BOOT0 = Port()
    PB8 = Port()
    PB9 = Port()
    PE0 = Port()
    PE1 = Port()
    VSS = Port()
    PDR_ON = Port()
    symbol = SymbolSTM32H725ZGTx()
    mappings = [
        SymbolMapping({
            PE2: symbol.PE2, 
            PE3: symbol.PE3, 
            PE4: symbol.PE4, 
            PE5: symbol.PE5, 
            PE6: symbol.PE6, 
            VDD[0]: symbol.VDD[0], 
            VBAT: symbol.VBAT, 
            PC13: symbol.PC13, 
            PC14: symbol.PC14, 
            PC15: symbol.PC15, 
            VDD[1]: symbol.VDD[1], 
            VSSSMPS: symbol.VSSSMPS, 
            VLXSMPS: symbol.VLXSMPS, 
            VDDSMPS: symbol.VDDSMPS, 
            VFBSMPS: symbol.VFBSMPS, 
            VDD[2]: symbol.VDD[2], 
            PF6: symbol.PF6, 
            PF7: symbol.PF7, 
            PF8: symbol.PF8, 
            PF9: symbol.PF9, 
            PF10: symbol.PF10, 
            PH0: symbol.PH0, 
            PH1: symbol.PH1, 
            NRST: symbol.NRST, 
            PC0: symbol.PC0, 
            PC1: symbol.PC1, 
            PC2_C: symbol.PC2_C, 
            PC3_C: symbol.PC3_C, 
            VDD[3]: symbol.VDD[3], 
            VSSA: symbol.VSSA, 
            VREFp: symbol.VREFp, 
            VDDA: symbol.VDDA, 
            PA0: symbol.PA0, 
            PA1: symbol.PA1, 
            PA2: symbol.PA2, 
            PA3: symbol.PA3, 
            VDD[4]: symbol.VDD[4], 
            PA4: symbol.PA4, 
            PA5: symbol.PA5, 
            PA6: symbol.PA6, 
            PA7: symbol.PA7, 
            PC4: symbol.PC4, 
            PC5: symbol.PC5, 
            PB0: symbol.PB0, 
            PB1: symbol.PB1, 
            PB2: symbol.PB2, 
            PF11: symbol.PF11, 
            PF14: symbol.PF14, 
            PF15: symbol.PF15, 
            VDD[5]: symbol.VDD[5], 
            PE7: symbol.PE7, 
            PE8: symbol.PE8, 
            PE9: symbol.PE9, 
            PE10: symbol.PE10, 
            PE11: symbol.PE11, 
            PE12: symbol.PE12, 
            PE13: symbol.PE13, 
            PE14: symbol.PE14, 
            PE15: symbol.PE15, 
            PB10: symbol.PB10, 
            PB11: symbol.PB11, 
            VCAP[0]: symbol.VCAP[0], 
            VDDLDO[0]: symbol.VDDLDO[0], 
            VDD[6]: symbol.VDD[6], 
            PB12: symbol.PB12, 
            PB13: symbol.PB13, 
            PB14: symbol.PB14, 
            PB15: symbol.PB15, 
            PD8: symbol.PD8, 
            PD9: symbol.PD9, 
            PD10: symbol.PD10, 
            VDD[7]: symbol.VDD[7], 
            PD11: symbol.PD11, 
            PD12: symbol.PD12, 
            PD13: symbol.PD13, 
            PD14: symbol.PD14, 
            PD15: symbol.PD15, 
            PG6: symbol.PG6, 
            PG7: symbol.PG7, 
            PG8: symbol.PG8, 
            VDD50USB: symbol.VDD50USB, 
            VDD33USB: symbol.VDD33USB, 
            VDD[8]: symbol.VDD[8], 
            PC6: symbol.PC6, 
            PC7: symbol.PC7, 
            PC8: symbol.PC8, 
            PC9: symbol.PC9, 
            PA8: symbol.PA8, 
            PA9: symbol.PA9, 
            PA10: symbol.PA10, 
            PA11: symbol.PA11, 
            PA12: symbol.PA12, 
            PA13JTMS: symbol.PA13JTMS, 
            VCAP[1]: symbol.VCAP[1], 
            VDDLDO[1]: symbol.VDDLDO[1], 
            VDD[9]: symbol.VDD[9], 
            PA14JTCK: symbol.PA14JTCK, 
            PA15JTDI: symbol.PA15JTDI, 
            PC10: symbol.PC10, 
            PC11: symbol.PC11, 
            PC12: symbol.PC12, 
            PD0: symbol.PD0, 
            PD1: symbol.PD1, 
            PD2: symbol.PD2, 
            PD3: symbol.PD3, 
            PD4: symbol.PD4, 
            PD5: symbol.PD5, 
            VDD[10]: symbol.VDD[10], 
            PD6: symbol.PD6, 
            PD7: symbol.PD7, 
            PG9: symbol.PG9, 
            PG10: symbol.PG10, 
            PG11: symbol.PG11, 
            PG12: symbol.PG12, 
            PG13: symbol.PG13, 
            PG14: symbol.PG14, 
            VDD[11]: symbol.VDD[11], 
            PB3JTDO: symbol.PB3JTDO, 
            PB4NJTRST: symbol.PB4NJTRST, 
            PB5: symbol.PB5, 
            PB6: symbol.PB6, 
            PB7: symbol.PB7, 
            BOOT0: symbol.BOOT0, 
            PB8: symbol.PB8, 
            PB9: symbol.PB9, 
            PE0: symbol.PE0, 
            PE1: symbol.PE1, 
            VCAP[2]: symbol.VCAP[2], 
            VSS: symbol.VSS, 
            PDR_ON: symbol.PDR_ON, 
            VDDLDO[2]: symbol.VDDLDO[2], 
            VDD[12]: symbol.VDD[12]
        }),
        PadMapping({
            PE2: landpattern.p[1],
            PE3: landpattern.p[2],
            PE4: landpattern.p[3],
            PE5: landpattern.p[4],
            PE6: landpattern.p[5],
            VDD[0]: landpattern.p[7],
            VBAT: landpattern.p[8],
            PC13: landpattern.p[9],
            PC14: landpattern.p[10],
            PC15: landpattern.p[11],
            VDD[1]: landpattern.p[13],
            VSSSMPS: landpattern.p[14],
            VLXSMPS: landpattern.p[15],
            VDDSMPS: landpattern.p[16],
            VFBSMPS: landpattern.p[17],
            VDD[2]: landpattern.p[19],
            PF6: landpattern.p[20],
            PF7: landpattern.p[21],
            PF8: landpattern.p[22],
            PF9: landpattern.p[23],
            PF10: landpattern.p[24],
            PH0: landpattern.p[25],
            PH1: landpattern.p[26],
            NRST: landpattern.p[27],
            PC0: landpattern.p[28],
            PC1: landpattern.p[29],
            PC2_C: landpattern.p[30],
            PC3_C: landpattern.p[31],
            VDD[3]: landpattern.p[32],
            VSSA: landpattern.p[34],
            VREFp: landpattern.p[35],
            VDDA: landpattern.p[36],
            PA0: landpattern.p[37],
            PA1: landpattern.p[38],
            PA2: landpattern.p[39],
            PA3: landpattern.p[40],
            VDD[4]: landpattern.p[42],
            PA4: landpattern.p[43],
            PA5: landpattern.p[44],
            PA6: landpattern.p[45],
            PA7: landpattern.p[46],
            PC4: landpattern.p[47],
            PC5: landpattern.p[48],
            PB0: landpattern.p[49],
            PB1: landpattern.p[50],
            PB2: landpattern.p[51],
            PF11: landpattern.p[52],
            PF14: landpattern.p[53],
            PF15: landpattern.p[54],
            VDD[5]: landpattern.p[56],
            PE7: landpattern.p[57],
            PE8: landpattern.p[58],
            PE9: landpattern.p[59],
            PE10: landpattern.p[60],
            PE11: landpattern.p[61],
            PE12: landpattern.p[62],
            PE13: landpattern.p[63],
            PE14: landpattern.p[64],
            PE15: landpattern.p[65],
            PB10: landpattern.p[66],
            PB11: landpattern.p[67],
            VCAP[0]: landpattern.p[68],
            VDDLDO[0]: landpattern.p[70],
            VDD[6]: landpattern.p[71],
            PB12: landpattern.p[72],
            PB13: landpattern.p[73],
            PB14: landpattern.p[74],
            PB15: landpattern.p[75],
            PD8: landpattern.p[76],
            PD9: landpattern.p[77],
            PD10: landpattern.p[78],
            VDD[7]: landpattern.p[79],
            PD11: landpattern.p[81],
            PD12: landpattern.p[82],
            PD13: landpattern.p[83],
            PD14: landpattern.p[84],
            PD15: landpattern.p[85],
            PG6: landpattern.p[86],
            PG7: landpattern.p[87],
            PG8: landpattern.p[88],
            VDD50USB: landpattern.p[90],
            VDD33USB: landpattern.p[91],
            VDD[8]: landpattern.p[92],
            PC6: landpattern.p[93],
            PC7: landpattern.p[94],
            PC8: landpattern.p[95],
            PC9: landpattern.p[96],
            PA8: landpattern.p[97],
            PA9: landpattern.p[98],
            PA10: landpattern.p[99],
            PA11: landpattern.p[100],
            PA12: landpattern.p[101],
            PA13JTMS: landpattern.p[102],
            VCAP[1]: landpattern.p[103],
            VDDLDO[1]: landpattern.p[105],
            VDD[9]: landpattern.p[106],
            PA14JTCK: landpattern.p[107],
            PA15JTDI: landpattern.p[108],
            PC10: landpattern.p[109],
            PC11: landpattern.p[110],
            PC12: landpattern.p[111],
            PD0: landpattern.p[112],
            PD1: landpattern.p[113],
            PD2: landpattern.p[114],
            PD3: landpattern.p[115],
            PD4: landpattern.p[116],
            PD5: landpattern.p[117],
            VDD[10]: landpattern.p[119],
            PD6: landpattern.p[120],
            PD7: landpattern.p[121],
            PG9: landpattern.p[122],
            PG10: landpattern.p[123],
            PG11: landpattern.p[124],
            PG12: landpattern.p[125],
            PG13: landpattern.p[126],
            PG14: landpattern.p[127],
            VDD[11]: landpattern.p[129],
            PB3JTDO: landpattern.p[130],
            PB4NJTRST: landpattern.p[131],
            PB5: landpattern.p[132],
            PB6: landpattern.p[133],
            PB7: landpattern.p[134],
            BOOT0: landpattern.p[135],
            PB8: landpattern.p[136],
            PB9: landpattern.p[137],
            PE0: landpattern.p[138],
            PE1: landpattern.p[139],
            VCAP[2]: landpattern.p[140],
            VSS: [
                landpattern.p[141],
                landpattern.p[128],
                landpattern.p[118],
                landpattern.p[104],
                landpattern.p[89],
                landpattern.p[80],
                landpattern.p[69],
                landpattern.p[55],
                landpattern.p[41],
                landpattern.p[33],
                landpattern.p[18],
                landpattern.p[12],
                landpattern.p[6],
            ],
            PDR_ON: landpattern.p[142],
            VDDLDO[2]: landpattern.p[143],
            VDD[12]: landpattern.p[144],
        }),
    ]

Device: type[STM32H725ZGT] = STM32H725ZGT
