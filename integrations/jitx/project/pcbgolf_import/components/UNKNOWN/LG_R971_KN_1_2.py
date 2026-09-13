# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/LG_R971_KN_1_2.py 
# To import this component:
#     from .components.UNKNOWN import LG_R971_KN_1_2
#     u1 = LG_R971_KN_1_2.LG_R971_KN_1()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternCHIPLED import LandpatternCHIPLED
from ...symbols.Symbolcomma_ai_11112255_LED_0805_1 import Symbolcomma_ai_11112255_LED_0805
class LG_R971_KN_1(Component):
    description = ""
    mpn = "LG R971-KN-1"
    datasheet = ""
    reference_designator_prefix = "LED"
    landpattern = LandpatternCHIPLED()
    A = Port()
    C = Port()
    symbol = Symbolcomma_ai_11112255_LED_0805()
    mappings = [
        SymbolMapping({
            A: symbol.A, 
            C: symbol.C
        }),
        PadMapping({
            A: landpattern.A,
            C: landpattern.C,
        }),
    ]

Device: type[LG_R971_KN_1] = LG_R971_KN_1
