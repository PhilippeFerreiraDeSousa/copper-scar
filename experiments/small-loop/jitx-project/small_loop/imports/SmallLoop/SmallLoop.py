# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/SmallLoop.py 
from jitx.circuit import Circuit
from jitx.net import Port, Net
from jitx.transform import Transform


from .components.UNKNOWN import QS5K2TR as QS5K2TR
class Main_01(Circuit):
    U_CH1_SBU1_IGN = Port()
    U_CH1_SBU1_RELAY = Port()
    U_GND = Port()
    U_Net__Q2_D1_ = Port()
    U_Net__Q2_D2_ = Port()

    Q2 = QS5K2TR.Device()

    nets = [
        Net([U_CH1_SBU1_IGN, Q2.G1], name="CH1_SBU1_IGN"),
        Net([U_CH1_SBU1_RELAY, Q2.G2], name="CH1_SBU1_RELAY"),
        Net([U_GND, Q2.S], name="GND"),
        Net([U_Net__Q2_D1_, Q2.D1], name="Net_Q2_D1"),
        Net([U_Net__Q2_D2_, Q2.D2], name="Net_Q2_D2"),
    ]

    def __init__(self):
        self.place(self.Q2, Transform((0, 0)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
class Main_02(Circuit):
    U_GND = Port()
    U_Net__LED10_AG_ = Port()
    U_Net__LED10_AR_ = Port()

    LED10 = AM23ESGW.Device()

    nets = [
        Net([U_GND, LED10.C], name="GND"),
        Net([U_Net__LED10_AG_, LED10.AG], name="Net_LED10_AG"),
        Net([U_Net__LED10_AR_, LED10.AR], name="Net_LED10_AR"),
    ]

    def __init__(self):
        self.place(self.LED10, Transform((0, 0)))



from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
class Main_03(Circuit):
    U_CH1_SBU1_RELAY = Port()
    U_GND = Port()

    R98 = RC0402FR_0710KL.Device()

    nets = [
        Net([U_CH1_SBU1_RELAY, R98.p[2]], name="CH1_SBU1_RELAY"),
        Net([U_GND, R98.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.R98, Transform((0, 0)))



from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Main_04(Circuit):
    U_CH1_SBU1 = Port()
    U_Net__Q2_D2_ = Port()

    R91 = RC0402JR_07100RL.Device()

    nets = [
        Net([U_CH1_SBU1, R91.p[2]], name="CH1_SBU1"),
        Net([U_Net__Q2_D2_, R91.p[1]], name="Net_Q2_D2"),
    ]

    def __init__(self):
        self.place(self.R91, Transform((0, 0)))



from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
class Main_05(Circuit):
    U_CH1_SBU1 = Port()
    U_Net__Q2_D1_ = Port()

    R90 = RC0402JR_071KL.Device()

    nets = [
        Net([U_CH1_SBU1, R90.p[2]], name="CH1_SBU1"),
        Net([U_Net__Q2_D1_, R90.p[1]], name="Net_Q2_D1"),
    ]

    def __init__(self):
        self.place(self.R90, Transform((0, 0)))



from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Main_06(Circuit):
    U_CH1_SBU1_IGN = Port()
    U_Net__LED10_AR_ = Port()

    R83 = RC0402JR_07100RL.Device()

    nets = [
        Net([U_CH1_SBU1_IGN, R83.p[2]], name="CH1_SBU1_IGN"),
        Net([U_Net__LED10_AR_, R83.p[1]], name="Net_LED10_AR"),
    ]

    def __init__(self):
        self.place(self.R83, Transform((0, 0)))



from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Main_07(Circuit):
    U_CH1_SBU1_RELAY = Port()
    U_Net__LED10_AG_ = Port()

    R82 = RC0402JR_07100RL.Device()

    nets = [
        Net([U_CH1_SBU1_RELAY, R82.p[2]], name="CH1_SBU1_RELAY"),
        Net([U_Net__LED10_AG_, R82.p[1]], name="Net_LED10_AG"),
    ]

    def __init__(self):
        self.place(self.R82, Transform((0, 0)))



from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
class Main_08(Circuit):
    U_CH1_SBU1_IGN = Port()
    U_GND = Port()

    R78 = RC0402FR_0710KL.Device()

    nets = [
        Net([U_CH1_SBU1_IGN, R78.p[1]], name="CH1_SBU1_IGN"),
        Net([U_GND, R78.p[2]], name="GND"),
    ]

    def __init__(self):
        self.place(self.R78, Transform((0, 0)))



from .components.UNKNOWN import RC0402JR_073K3L as RC0402JR_073K3L
class Main_09(Circuit):
    U_EXT_5V = Port()
    U_Net__LED6_PadA_ = Port()

    R74 = RC0402JR_073K3L.Device()

    nets = [
        Net([U_EXT_5V, R74.p[1]], name="EXT_5V"),
        Net([U_Net__LED6_PadA_, R74.p[2]], name="Net_LED6_PadA"),
    ]

    def __init__(self):
        self.place(self.R74, Transform((0, 0)))



from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
class Main_10(Circuit):
    U_CH1_SBU1 = Port()
    U_EXT_SENSE = Port()

    R19 = RC0402JR_07100KL.Device()

    nets = [
        Net([U_CH1_SBU1, R19.p[2]], name="CH1_SBU1"),
        Net([U_EXT_SENSE, R19.p[1]], name="EXT_SENSE"),
    ]

    def __init__(self):
        self.place(self.R19, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
class Main_11(Circuit):
    U_EXT_5V = Port()
    U_GND = Port()

    C5 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([U_EXT_5V, C5.p[1]], name="EXT_5V"),
        Net([U_GND, C5.p[2]], name="GND"),
    ]

    def __init__(self):
        self.place(self.C5, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
class Main_12(Circuit):
    U_EXT_5V = Port()
    U_GND = Port()

    C46 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([U_EXT_5V, C46.p[1]], name="EXT_5V"),
        Net([U_GND, C46.p[2]], name="GND"),
    ]

    def __init__(self):
        self.place(self.C46, Transform((0, 0)))



from .components.UNKNOWN import comma_ai_11112255_M2X4 as comma_ai_11112255_M2X4
class Main_13(Circuit):
    U_CH1_SBU1 = Port()
    U_CH1_SBU1_IGN = Port()
    U_CH1_SBU1_RELAY = Port()
    U_EXT_5V = Port()
    U_EXT_SENSE = Port()
    U_GND = Port()

    J4 = comma_ai_11112255_M2X4.Device()

    nets = [
        Net([U_CH1_SBU1, J4.p[5]], name="CH1_SBU1"),
        Net([U_CH1_SBU1_IGN, J4.p[3]], name="CH1_SBU1_IGN"),
        Net([U_CH1_SBU1_RELAY, J4.p[4]], name="CH1_SBU1_RELAY"),
        Net([U_EXT_5V, J4.p[2], J4.p[7]], name="EXT_5V"),
        Net([U_EXT_SENSE, J4.p[6]], name="EXT_SENSE"),
        Net([U_GND, J4.p[1], J4.p[8]], name="GND"),
    ]

    def __init__(self):
        self.place(self.J4, Transform((0, 0)))

        self.J4.x_out = True


from .components.UNKNOWN import CL21A106KAYNNNE as CL21A106KAYNNNE
class Main_14(Circuit):
    U_EXT_5V = Port()
    U_GND = Port()

    C50 = CL21A106KAYNNNE.Device()

    nets = [
        Net([U_EXT_5V, C50.p[1]], name="EXT_5V"),
        Net([U_GND, C50.p[2]], name="GND"),
    ]

    def __init__(self):
        self.place(self.C50, Transform((0, 0)))



from .components.UNKNOWN import LG_R971_KN_1 as LG_R971_KN_1
class Main_15(Circuit):
    U_GND = Port()
    U_Net__LED6_PadA_ = Port()

    LED6 = LG_R971_KN_1.Device()

    nets = [
        Net([U_GND, LED6.C], name="GND"),
        Net([U_Net__LED6_PadA_, LED6.A], name="Net_LED6_PadA"),
    ]

    def __init__(self):
        self.place(self.LED6, Transform((0, 0)))



class Main(Circuit):
    Main_01 = Main_01()
    Main_02 = Main_02()
    Main_03 = Main_03()
    Main_04 = Main_04()
    Main_05 = Main_05()
    Main_06 = Main_06()
    Main_07 = Main_07()
    Main_08 = Main_08()
    Main_09 = Main_09()
    Main_10 = Main_10()
    Main_11 = Main_11()
    Main_12 = Main_12()
    Main_13 = Main_13()
    Main_14 = Main_14()
    Main_15 = Main_15()

    nets = [
        Net([Main_04.U_CH1_SBU1, Main_05.U_CH1_SBU1, Main_10.U_CH1_SBU1, Main_13.U_CH1_SBU1], name="CH1_SBU1"),
        Net([Main_01.U_CH1_SBU1_IGN, Main_06.U_CH1_SBU1_IGN, Main_08.U_CH1_SBU1_IGN, Main_13.U_CH1_SBU1_IGN], name="CH1_SBU1_IGN"),
        Net([Main_01.U_CH1_SBU1_RELAY, Main_03.U_CH1_SBU1_RELAY, Main_07.U_CH1_SBU1_RELAY, Main_13.U_CH1_SBU1_RELAY], name="CH1_SBU1_RELAY"),
        Net([Main_09.U_EXT_5V, Main_11.U_EXT_5V, Main_12.U_EXT_5V, Main_13.U_EXT_5V, Main_14.U_EXT_5V], name="EXT_5V"),
        Net([Main_10.U_EXT_SENSE, Main_13.U_EXT_SENSE], name="EXT_SENSE"),
        Net([Main_01.U_GND, Main_02.U_GND, Main_03.U_GND, Main_08.U_GND, Main_11.U_GND, Main_12.U_GND, Main_13.U_GND, Main_14.U_GND, Main_15.U_GND], name="GND"),
        Net([Main_02.U_Net__LED10_AG_, Main_07.U_Net__LED10_AG_], name="Net_LED10_AG"),
        Net([Main_02.U_Net__LED10_AR_, Main_06.U_Net__LED10_AR_], name="Net_LED10_AR"),
        Net([Main_09.U_Net__LED6_PadA_, Main_15.U_Net__LED6_PadA_], name="Net_LED6_PadA"),
        Net([Main_01.U_Net__Q2_D1_, Main_05.U_Net__Q2_D1_], name="Net_Q2_D1"),
        Net([Main_01.U_Net__Q2_D2_, Main_04.U_Net__Q2_D2_], name="Net_Q2_D2"),
    ]

    def __init__(self):
        self.place(self.Main_01, Transform((-67, 118.5)))
        self.place(self.Main_02, Transform((-51, 109.5)))
        self.place(self.Main_03, Transform((-51, 118.5)))
        self.place(self.Main_04, Transform((-59, 109.5)))
        self.place(self.Main_05, Transform((-67, 109.5)))
        self.place(self.Main_06, Transform((-75, 109.5)))
        self.place(self.Main_07, Transform((-43, 118.5)))
        self.place(self.Main_08, Transform((-59, 118.5)))
        self.place(self.Main_09, Transform((-75, 100.5)))
        self.place(self.Main_10, Transform((-51, 100.5)))
        self.place(self.Main_11, Transform((-43, 100.5)))
        self.place(self.Main_12, Transform((-67, 100.5)))
        self.place(self.Main_13, Transform((-75, 118.5)))
        self.place(self.Main_14, Transform((-59, 100.5)))
        self.place(self.Main_15, Transform((-43, 109.5)))

        self.Main_01.Q2.reference_designator = "Q2"
        self.Main_02.LED10.reference_designator = "LED10"
        self.Main_03.R98.reference_designator = "R98"
        self.Main_04.R91.reference_designator = "R91"
        self.Main_05.R90.reference_designator = "R90"
        self.Main_06.R83.reference_designator = "R83"
        self.Main_07.R82.reference_designator = "R82"
        self.Main_08.R78.reference_designator = "R78"
        self.Main_09.R74.reference_designator = "R74"
        self.Main_10.R19.reference_designator = "R19"
        self.Main_11.C5.reference_designator = "C5"
        self.Main_12.C46.reference_designator = "C46"
        self.Main_13.J4.reference_designator = "J4"
        self.Main_14.C50.reference_designator = "C50"
        self.Main_15.LED6.reference_designator = "LED6"


