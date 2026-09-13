# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/components/UNKNOWN/RC0402FR_0710KL.py 
# To import this component:
#     from .components.UNKNOWN import RC0402FR_0710KL
#     u1 = RC0402FR_0710KL.RC0402FR_0710KL()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_R import LandpatternU0402_R
from ...symbols.Symbolcomma_ai_11112255_R0402_2 import Symbolcomma_ai_11112255_R0402
class RC0402FR_0710KL(Component):
    description = ""
    mpn = "RC0402FR-0710KL"
    datasheet = ""
    reference_designator_prefix = "R"
    landpattern = LandpatternU0402_R()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_R0402()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[2],
        }),
    ]

Device: type[RC0402FR_0710KL] = RC0402FR_0710KL
