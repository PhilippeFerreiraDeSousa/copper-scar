# Real PCBGolf baseline and native validation

Updated September 12, 2026. This supersedes simulation-only planning: the intended
outcome is an actual valid, smaller PCB. The simulator is an early loop prototype,
not a qualified board design. This document records the initial investigation;
the subsequent install and actual native results are in [native-checks.md](native-checks.md).

## Source baseline

Official repository: https://github.com/commaai/PCBGolf

Local immutable starting checkout: `/Users/philippe/dev/PCBGolf`, commit
`7210bdb5049c5b7fdf4900a34928e2736767292a`.

Static source inspection found 245 footprints, 1,053 pad-net assignments and 302
distinct net strings, with two enabled copper layers. There are no track, via,
zone or top-level board-outline graphics. This is an unrouted starting design,
not a valid manufactured baseline with a score we can already improve.

The project uses KiCad 10 format and explicitly lists five `top_level_sheets`:
Power, STM32H7, USB + SD, CAN-FD and Channels. Preserve all five `.kicad_sch` files,
`pcbgolf.kicad_pro`, custom library tables, symbols, footprints and 3D models.
All 26 unique referenced STEP paths exist, used by 240 footprints. J4 (2X04) and
BH1–BH4 have no model assignments. Review actual population and model completeness
before claiming an assembled bounding box; do not silently omit a fitted header.

The project contains global DRC rules, severity settings, one Default netclass,
no exclusions and no custom `.kicad_dru`. These are starting constraints, not a
complete specification of current JLCPCB capability or electrical performance.
The challenge also requires assembly, functionality, usability and mating
connector compatibility. Native ERC/DRC alone does not prove those properties.

## Copperhead runs real KiCad checks

Inspected source: copperheadhq/copperhead commit
`ef5a129f13b35e67b98216ea2f09aa7739ce6798` (package 0.10.0).

With Copperhead installed and `.copperhead/config.json` pointing to the existing
files, its entry point is:

```bash
copperhead --repo /absolute/path/to/candidate --json check
```

`verify` is an alias. The check command does not use an LLM or need a model key.
It also checks document drift and other configured checks. Prerequisites include
Node >=20 and KiCad; Copperhead's doctor accepts KiCad >=8, but this board needs
KiCad 10. `COPPERHEAD_KICAD_CLI` can point to the full executable path.

The minimal relevant configuration fields are:

```json
{
  "schematic": "pcbgolf.kicad_sch",
  "board": "pcbgolf.kicad_pcb",
  "docs": "docs"
}
```

The wrapper invokes real commands equivalent to:

```bash
kicad-cli sch erc --format json --exit-code-violations --output /tmp/erc.json /absolute/path/to/candidate/pcbgolf.kicad_sch
kicad-cli pcb drc --format json --exit-code-violations --output /tmp/drc.json /absolute/path/to/candidate/pcbgolf.kicad_pcb
```

It passes the original design path, rather than converting the board or copying
it away from its project. Keep the original basename-matched `.kicad_pro` and any
future `.kicad_dru` beside the candidate board so native KiCad resolves them.
Copperhead itself neither translates nor verifies preservation of those rules.

Material limits of the inspected wrapper:

- DRC does not request `--schematic-parity` or `--refill-zones`.
- Config has one schematic string. Confirm KiCad 10's report covers all five
  top-level sheets. Do not equate one configured filename with proven coverage.
- Missing/unconfigured schematic or board is skipped, and overall `ok` can still
  be true. Require both report fields to be non-null in any integration.
- Native JSON is normalized from ERC sheets, DRC violations, unconnected items
  and schematic-parity items. Any returned violation, including a warning, fails.
- A missing or unreadable JSON report throws. However, a parsed report is
  normalized without checking the process exit code or validating its schema;
  an unexpected empty object could appear clean. Retain raw output and exit codes
  in the Copper Scar gate rather than trusting only this summary.
- Temporary raw reports are deleted after normalization. Its JSON check output
  contains ERC/DRC counts, not a retained full native report.

Source references:

- [Native command wrapper](https://github.com/copperheadhq/copperhead/blob/ef5a129f13b35e67b98216ea2f09aa7739ce6798/src/kicad/cli.ts#L261)
- [Command entry point](https://github.com/copperheadhq/copperhead/blob/ef5a129f13b35e67b98216ea2f09aa7739ce6798/src/cli.ts#L161)
- [Skip and aggregation behavior](https://github.com/copperheadhq/copperhead/blob/ef5a129f13b35e67b98216ea2f09aa7739ce6798/src/commands/check.ts#L45)
- [Report normalization](https://github.com/copperheadhq/copperhead/blob/ef5a129f13b35e67b98216ea2f09aa7739ce6798/src/kicad/report.ts#L48)

## Validate a JITX-exported candidate against original rules

Make a candidate copy of the entire official project. Replace only its
`pcbgolf.kicad_pcb` with the exported layout, keeping the original project,
schematics, rules and libraries. Do not overwrite them with export defaults.
Confirm layer names/counts, net names and reference/pad identities still map to
the original definitions. Pin mapping changes require explicit equivalence
checks; a translation mismatch is not permission to suppress parity failures.

From that candidate directory, the native check entry points are:

```bash
mkdir -p reports
kicad-cli version
kicad-cli sch erc --format json --severity-all --exit-code-violations \
  --output reports/erc.json pcbgolf.kicad_sch
kicad-cli pcb drc --format json --severity-all --all-track-errors \
  --schematic-parity --refill-zones --exit-code-violations \
  --output reports/drc.json pcbgolf.kicad_pcb
```

These flags are documented in the [KiCad 10 CLI manual](https://docs.kicad.org/10.0/en/cli/cli.html).
These were initially unexecuted; the installed KiCad 10.0.6 results and multi-root
coverage limitation are now recorded in `native-checks.md`. Record each
exit status and stdout/stderr; require a well-formed report and explicit sheet
coverage. Run additional per-sheet ERC as needed if the first report omits any
project root. `--refill-zones` recomputes fills; omit `--save-board` for an audit.

Also export and compare original versus candidate connectivity as sets of
(reference, pad number) per net across all five schematics. Preserve original
BOM/functionality and add explicit routing constraints for critical interfaces,
power paths and return paths. Recheck manufacturer constraints against the chosen
stackup. Treat real DRC failures as candidate rejection or an unresolved baseline
issue, never as a signal to turn a rule off.

Only after a complete routed, closed-outline candidate exists, export assembled
STEP with components, verify all populated models and transforms, and compute
`(xmax-xmin)*(ymax-ymin)*(zmax-zmin) + 50*vias + 5000*copper_layers` from the actual
assembly envelope and board. Board thickness alone is not assembly height.
A CAD bounding-box tool and a model-completeness check remain prerequisites.

## Tool status and reusable pieces

At initial inspection KiCad / FreeCAD were absent and Docker's engine socket was
absent. KiCad has since been installed per-user and native checks captured; see
`native-checks.md`. No complete routing or qualified real-board score exists.

JITX 4.4.0 CLI is installed in the isolated probe at
`/Users/philippe/dev/copper-scar-jitx/.venv`. Runtime setup is separate. Its actual
CLI advertises `design export legacy-kicad` and `legacy-step`; this is command
availability, not a successful round trip. Official docs support macOS and
Python >=3.12. [The free plan](https://www.jitx.com/plans) specifies CERN OHL-P
v2 open designs; no account or licensing terms have been accepted here.

Copperhead's source calls its layout stage a first draft and can leave uncritical
nets unrouted. tscircuit's CLI import code and examples show component/footprint
imports; a lossless full KiCad 10 project import has not been demonstrated.
No tool has yet passed this project's real-board acceptance checks.

Reuse Copper Scar's score arithmetic, trace/eval structure and the concept of
persisting rejected-candidate constraints. Replace the rectangle board model,
hand-coded placement actions, inferred gate flags and synthetic dataset as the
source of real PCB validity. Establish a fully routed valid baseline before
running bounded candidate edits and accepting only measured, valid improvements.

## Existing JLCPCB rule decks

Copperhead's inspected source has a JLCPCB assembly-BOM exporter, but no bundled
JLCPCB `.kicad_dru` or manufacturer capability profile was found. Native KiCad
checks will use a supplied project rule deck; Copperhead need not implement a
new checker for this.

The most current starter located is [Cimos/kicad-druid](https://github.com/Cimos/kicad-druid),
inspected at `8af046d6a1839320a360a4b6790ac11eb27a78ae` (September 3, 2026).
It supplies generated rule variants and test boards. GitHub showed a successful
lint run at that head and a successful DRC workflow at `02782fc3`, the preceding
commit; those are remote checks, not local validation here.

Available variants include 2L/1oz, 4L/1oz, 4L/2oz and 6L/1oz. Its plain
`JLCPCB.kicad_dru` is the 4L/1oz default, so do not accidentally apply that to the
current two-layer baseline. A candidate 2L/1oz deck, IF those fabrication options
are chosen, is [JLCPCB-2L-1oz.kicad_dru](https://github.com/Cimos/kicad-druid/blob/8af046d6a1839320a360a4b6790ac11eb27a78ae/JLCPCB/JLCPCB-2L-1oz.kicad_dru).
Copy the chosen file as `pcbgolf.kicad_dru` beside the project and retain it across
candidate exports. Keep required original constraints and review custom-rule
precedence; do not replace original rules blindly or use a looser custom rule to
bypass an electrical requirement.

This is third-party work, not a JLCPCB-certified rule deck. It contains inferred
clearances and cost-avoidance rules. Spot checks against
[JLCPCB's current capability table](https://jlcpcb.com/capabilities/pcb-capabilities)
confirmed its 2L/1oz 0.10mm trace/spacing, multilayer/1oz 0.09mm and routed-edge
0.20mm values. Other cases still need review: the TOML uses 0.20mm pad-to-track
clearance while the general current fab table states 0.10mm; its SMD minimum
0.125mm interpretation differs from the table's stated 0.25×0.25mm minimum.
The first is conservative; the second needs supporting capability clarification
before relying on it. Color, copper weight, finish, holes/slots and assembly
options matter. A deck does not validate electrical functionality, actual
impedance, power/thermal limits, connector access or complete assembly DFM.

Older alternatives:

- [labtroll/KiCad-DesignRules](https://github.com/labtroll/KiCad-DesignRules):
  paired PASS/FAIL board; latest commit November 29, 2024.
- [tinfever's JLCPCB rules and tests](https://github.com/tinfever/KiCAD-Custom-DRC-Rules-for-JLCPCB-with-Unit-Tests):
  explicitly 4-layer; latest commit July 6, 2023.

Recommendation: reuse a pinned, reviewed variant and its fixtures; compare the
selected process against primary JLCPCB specs and add only missing project
constraints. No fabrication option or deck has been selected/applied yet.

JITX setup update: the official macOS 4.4.0 runtime installation completed and
`jitx runtime introspect` confirmed version 4.4.0. Account activation, importing
the official board and exporting a checked candidate remain unperformed. The
installed CLI supports browser login via `jitx auth login`; this is a user step
if an account must be created or terms accepted.
