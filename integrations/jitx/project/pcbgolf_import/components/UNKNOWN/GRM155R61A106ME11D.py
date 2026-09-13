# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/GRM155R61A106ME11D.py 
# To import this component:
#     from .components.UNKNOWN import GRM155R61A106ME11D
#     u1 = GRM155R61A106ME11D.GRM155R61A106ME11D()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_C import LandpatternU0402_C
from ...symbols.Symbolcomma_ai_11112255_C0402_1 import Symbolcomma_ai_11112255_C0402
class GRM155R61A106ME11D(Component):
    description = ""
    mpn = "GRM155R61A106ME11D"
    datasheet = ""
    reference_designator_prefix = "C"
    landpattern = LandpatternU0402_C()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_C0402()
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

Device: type[GRM155R61A106ME11D] = GRM155R61A106ME11D
