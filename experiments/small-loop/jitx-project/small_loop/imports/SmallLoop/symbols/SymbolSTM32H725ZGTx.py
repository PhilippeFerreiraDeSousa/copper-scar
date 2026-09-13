# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolSTM32H725ZGTx.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.composites import rectangle


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
    draw = rectangle(68, 140)

