# Assembly readiness audit

These scripts read an isolated copy of a frozen KiCad board. They do not save or modify CAD, change component poses, invent missing bodies, or qualify a finished product.

1. Copy the accepted `pcbgolf.kicad_pcb` and `pcbgolf.kicad_pro` into a private output directory. Copy the original `pcbgolf.3dshapes` alongside them so existing `${KIPRJMOD}` references resolve unchanged. Record source and copied file hashes.
2. Run `inventory.py INPUT/pcbgolf.kicad_pcb --original ORIGINAL_PCBGOLF --output model-coverage.json` using the Python interpreter bundled with KiCad. The inventory checks original DNP flags and each supplied model's hash, visibility and transform. No GUI is opened. Native Python may emit wx initialization diagnostics; inspect its exit status and output.
3. Run `kicad-cli pcb export step --no-dnp --cut-vias-in-body --output recorded-population-unqualified.step INPUT/pcbgolf.kicad_pcb`. Save the exact command, CLI version, stdout/stderr and STEP hash. This honors recorded DNP flags; it is not permission to change the intended assembly BOM.
4. In an isolated Python 3.12 environment with `cadquery-ocp==8.0.1.0.0`, run `verify_step.py recorded-population-unqualified.step --inventory model-coverage.json --output step-geometry-check.json`. It compares top-level component names to the recorded population, independently reads the STEP, checks solids and computes the actual exported geometry bounds. Nested manufacturer-model labels are not board component instances.
5. Recheck every copied input hash and authoritative board/project bytes after export. Keep all runtime files outside Git.

The accepted 52-open audit found 245 footprints, 240 model references and 26 unique supplied models. Seven DNP references were preserved from the original: BH1–BH4, C6, C10 and J4. All 238 populated footprints resolved to original models. BH1–BH4 are grounded plated mounting-hole features, not unspecified populated bolt bodies. J4 is an unpopulated 2×4 CAN header footprint with no specified manufacturer part or model. Populating it later requires actual part/mating requirements; a generic connector body is not evidence of compatibility.

Complete model coverage for that recorded population does not establish collision clearance, mating access, soldering/rework access, PCB fabrication or functional correctness. The 52-open board is incomplete. Bounding volume is a geometry measurement of this export, never an official PCBGolf score or final submission claim.
