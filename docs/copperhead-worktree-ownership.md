# Copperhead worktree ownership

Verified 12 September 2026; bounded ownership/documentation task completed.

- Registered worktree: `/Users/philippe/dev/copper-scar-demo`.
- Branch: `codex/demo-takeover`.
- HEAD: `9b72b82f91b37d17314dcd281ccd90d31d6bf432`.
- Main checkout: `/Users/philippe/dev/copper-scar`, branch `main`, HEAD `27846f947b19588c271856001379e30da503ee1e`; read-only to this track, clean when inspected.
- JITX must use a different registered worktree, verified by its owning task. Copperhead does not create, change or assume ownership of it.

## Writes and environments

Initial documentation-task writes: `docs/copperhead-plan-and-design.md`, this record, and the requested review copy `/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/copperhead-plan-and-design.md`. Repository-relative paths here resolve only under the Copperhead worktree above.

Originally proposed Copperhead-owned code: `copper_scar/real.py`, native CLI sections, `tests/test_real.py`, `scripts/copperhead.sh`, `scripts/prepare-pcbgolf.sh`, native docs and the proposed `copper_scar/tools/copperhead/` adapter. Changes to common CLI, scoring, schemas, checker interfaces or dependency manifests must be assigned explicitly before editing. This record does not start that implementation work.

Dependencies: local `.venv/` and `node_modules/`; both roots verified non-symlink directories. Retain existing `.local/pcbgolf-candidate/` and `.local/checks/`. Future outputs are reserved to `.local/copperhead/candidates/<run-id>/` and `.local/copperhead/runs/<run-id>/`, with unique IDs; these directories need not be created until a run starts. `.local/pcbgolf-source/` remains a clean reference. No shared mutable generated outputs. Existing global KiCad may be invoked but not updated; no global installations or shared runtime updates.

## Architecture and boundaries

Copperhead/native and JITX own separate inner loops and checkers. JITX may translate constraints into native checks and defer export to selected checkpoints/final comparison. Speed and coverage equivalence require benchmarks. Independent KiCad comparison does not require a shared inner-loop implementation. Common checker work requires explicit coordination and one writer per change.

Worktrees are Git working-state isolation, not filesystem sandboxes. Same-user access and Git administrative state remain shared. Path ownership and hashes detect/prevent ordinary accidental overlap by workflow convention, not OS enforcement. No editing main, JITX code/docs/environments, or another track's candidates. No reset, clean, delete, merge or push.

## Preservation and status

The pre-existing modified `demos/pass_timeline.md` and untracked `demos/record-demo.sh` and `demos/weave-evidence.md` were preserved byte-for-byte. All pre-existing tracked and untracked non-ignored files other than the authorized plan were hash-compared after the update. Branch and HEAD were retained. The existing candidate's untracked `.copperhead/` configuration was left in place. No dependency installation, board edit, model call, routing run or implementation change was performed.

The initial bounded documentation task was completed. Later explicit authorization started native implementation and experiments, as recorded below. The canonical plan and review copy are synchronized.

## Subsequent implementation authorization

The user subsequently authorized completing Stage 1 as a durable native repair loop, local routing/tool dependencies and visible live observability. Current owned additions are `copper_scar/tools/copperhead/`, `scripts/copperhead_*.py`, focused tests and native-loop documentation. Candidate/run/tool/runtime data remains under `.local/copperhead/`; upstream sources and original reference remain preserved. No changes to common CLI, core checker or dependency manifests were needed for these additions. Native routing is active in bounded invocations; no valid baseline or Stage 2 result is claimed. The earlier preservation statement describes the initial documentation checkpoint, not a claim that no work happened afterward.

## GitHub checkpoint authorization

The user subsequently explicitly authorized committing and pushing completed Copperhead-owned work on `codex/demo-takeover`. This supersedes the earlier no-push boundary for this branch only. Pre-existing demo changes remain excluded; no merge into main, JITX edits, native binaries or bulky generated evidence are included. See `copperhead-reproduction.md` for retained local artifacts and dependency provenance. Placement-first realignment is sequenced after both tracks' remote checkpoints are confirmed by Main.
