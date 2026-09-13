# Offline JITX evidence package

`integrations/jitx/package_demo.py` packages completed original JITX runs without
contacting a runtime. Supply `--project`, `--outputs`, and `--dest`; it uses only
the Python standard library. Open the generated `index.html` directly.

The package demonstrates the eight-pad/four-net fixture: explicit six-via
two-layer routing, zero opens/violations, a TP4 move preserving three unrelated
nets, and source-authoritative placement persistence. The separate source-only
candidate declares ten Routes. Raw native net IDs renumber on rebuild; this is
not a claim of internal solver-state persistence.

The historical whole-board replay remains explicitly incomplete. Its fifteen
entries include eleven reliable evaluations, three failed attempts holding a
preceding board, and one unreliable evaluation. Final009 has310 missing
connections and44 physical errors, with no valid final score.

Packaging verifies original and normalized board hashes, project/source hashes,
both saved DRC reports per fixture stage, unaffected-net geometry, and every
historical replay snapshot hash. It copies portable KiCad boards/projects and
reports, not runtime caches. The separate joint integration report is attributed
existing evidence only; packaging does not inspect or retry that investigation.

September13 delivery QA also checked every relative HTML link, SVG XML,
SHA256 manifest and full H.264 decode (1920x1080,6seconds). Browser visual QA was
unavailable because browser security policy rejected the local file URL; no
workaround was attempted. Native routing and fresh DRC were not run for this
delivery, preserving the existing completed evidence.
