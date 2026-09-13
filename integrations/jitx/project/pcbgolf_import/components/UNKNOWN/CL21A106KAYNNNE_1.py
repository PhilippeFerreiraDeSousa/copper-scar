# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/CL21A106KAYNNNE_1.py 
# To import this component:
#     from .components.UNKNOWN import CL21A106KAYNNNE_1
#     u1 = CL21A106KAYNNNE_1.CL21A106KAYNNNE()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0805_C import LandpatternU0805_C
from ...symbols.Symbolcomma_ai_11112255_C0805 import Symbolcomma_ai_11112255_C0805
class CL21A106KAYNNNE(Component):
    description = ""
    mpn = "CL21A106KAYNNNE"
    datasheet = ""
    reference_designator_prefix = "C"
    landpattern = LandpatternU0805_C()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_C0805()
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

Device: type[CL21A106KAYNNNE] = CL21A106KAYNNNE
