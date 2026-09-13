# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/ABM8AIG_24_000MHZ_12_2Z_T3.py 
# To import this component:
#     from .components.UNKNOWN import ABM8AIG_24_000MHZ_12_2Z_T3
#     u1 = ABM8AIG_24_000MHZ_12_2Z_T3.ABM8AIG_24_000MHZ_12_2Z_T3()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternXTAL_3_2X2_5 import LandpatternXTAL_3_2X2_5
from ...symbols.Symbolcomma_ai_11112255_CRYSTAL_4PIN4_PIN_1 import Symbolcomma_ai_11112255_CRYSTAL_4PIN4_PIN
class ABM8AIG_24_000MHZ_12_2Z_T3(Component):
    description = ""
    mpn = "ABM8AIG-24.000MHZ-12-2Z-T3"
    datasheet = ""
    reference_designator_prefix = "Y"
    landpattern = LandpatternXTAL_3_2X2_5()
    p = {
        1: Port(),
        2: Port(),
        3: Port(),
    }
    symbol = Symbolcomma_ai_11112255_CRYSTAL_4PIN4_PIN()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2], 
            p[3]: symbol.p[3]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[3],
            p[3]: [
                landpattern.p[4],
                landpattern.p[2],
            ],
        }),
    ]

Device: type[ABM8AIG_24_000MHZ_12_2Z_T3] = ABM8AIG_24_000MHZ_12_2Z_T3
