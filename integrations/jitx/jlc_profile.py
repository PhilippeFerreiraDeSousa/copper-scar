"""JITX JLCPCB 2.0.0 profile reuse, with recorded source/current-fab corrections.
Four-layer proposal only. Circuit impedance/current rules remain separate obligations.
"""
from jitx.container import inline
from jitx.stackup import Conductor, Symmetric
from jitxlib.jlcpcb import JLC04161H_1080
from jitxlib.jlcpcb.rules import JLCPCBRules
from jitxlib.jlcpcb.materials import FR4_1080, FR4_Core, SoldermaskMaterial

class VerifiedJLCGenerationRules(JLCPCBRules):
    # Original minimum width .1016 > vendor multilayer .09.
    min_copper_width = 0.1016
    # .2 original netclass plus .05 measured exporter guard; not a rule relaxation.
    min_copper_copper_space = 0.25
    # Current JLC PTH-to-track .28 exceeds profile's undifferentiated .254.
    # Conservative global generation floor; type-specific external checks still required.
    min_copper_hole_space = 0.28
    # Original .0762 annular minimum < current multilayer PTH absolute .15.
    min_annular_ring = 0.15
    # Original imported bridge .102 and current common-color JLC .10 > profile .08.
    min_soldermask_bridge = 0.102

class VerifiedJLC04161H1080(JLC04161H_1080):
    # Reuse official substrate/vias/materials. Correct inner copper to manufacturer's
    # published .0152mm; package2.0.0 used .0175mm for this named stackup.
    @inline
    class stackup(Symmetric):
        soldermask = SoldermaskMaterial(thickness=0.01524)
        top = Conductor(thickness=0.035)
        prepreg = FR4_1080(thickness=0.0764)
        inner = Conductor(thickness=0.0152)
        core = FR4_Core(thickness=1.265)
    constraints = VerifiedJLCGenerationRules()
