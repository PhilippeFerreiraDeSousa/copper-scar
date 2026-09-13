# Preserved connector clearance conflict

The original footprint is named USB-C-FEMALE-VERT-GCT, but J5-J8 carry original MPN **Amphenol FCI 10132328-10011LF** and a matching relative STEP model. Do not infer manufacturer from the historical footprint name.

An isolated native DRC of the complete original source reproduces all 16 large-loop hole-clearance findings with the **same UUID pairs and same measured 0.2094 mm clearance**. Source rule `min_hole_clearance` remains 0.25 mm. A separate read-only native check compares every numbered electrical pad and unnumbered mechanical pad, including footprint-relative location/angle, dimensions, drill, type and layers: all 156 retained/aliased footprints pass. This rules out duplicated-hole, import-placement or project-save drift as the cause.

Each connector has two unnumbered NPTH holes, diameter 0.66 mm, centered locally at (-3.75,0) and (3.75,0). The implicated ground shield SMT pads are 1.03 x 0.50 mm: S11(-3.75,-1,39deg), S12(3.75,-1,321deg), S13(3.75,1,39deg), S14(-3.75,1,321deg). The conflict is **hole-to-copper**, not two drilled holes too close together. The source has two holes per connector; there are four ground-pad/hole violations per connector.

Official manufacturer drawing: https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/10132328.pdf (Rev B, drawing 10132328). The web-indexed drawing confirms this part family and contains 0.66 mm, 7.50 mm and 39-degree callouts. Direct downloads returned HTTP403; full visual dimensional verification of the recommended PCB pattern was not completed. **No manufacturer-qualified geometry repair is established.**

Recommendation: keep the current input frozen and explicitly unaccepted while placement/routing research continues. Do not shrink the holes, move shielding pads, change connector/BOM or relax the original rule based only on this DRC report. A later declared input revision needs the actual recommended-land-pattern comparison and, if that geometry is intentional, an explicit manufacturing/rule decision. No exception, constraint relaxation or geometry change has been applied to the experiment. The native loss retains 16 hole-clearance errors and 68 additional original internal silk-over-copper findings.

Local evidence: `.local/large-loop/connector-audit/source-copy/`, `source-drc.json`, `finding.json`; full geometry check in `.local/large-loop/v1/routing-control-01/full-geometry.json`. These are separate from immutable routing checkpoints.
