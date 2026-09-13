# JITX ownership and write boundaries

Verified 2026-09-12. Repository worktree: `/Users/philippe/dev/copper-scar-jitx-worktree`. Branch: `codex/jitx-optimization`. Base: `27846f947b19588c271856001379e30da503ee1e`.

Task metadata cwd remains `/Users/philippe/dev/copper-scar`; it is not the write target. Every future repository operation must specify the dedicated JITX worktree cwd/path explicitly. Main is an integration destination only.

JITX-owned repository writes: approach-specific implementation, tests and docs in this worktree. Completed changes include implementation, tests, project source and documentation. Owned implementation namespace: `integrations/jitx/`; coordinate any shared CLI, schema, scoring, dependency manifest or core-checker change with the core owner before editing. Core commit `9b72b82` is not present in this worktree by assumption; no merge/cherry-pick was performed.

Preserved external JITX project/environment: `/Users/philippe/dev/copper-scar-jitx`, including `.venv`, `pcbgolf_probe`, `.vscode` and docs. JITX-only future candidates: `/Users/philippe/dev/copper-scar-jitx/candidates/<attempt>`; runs: `/Users/philippe/dev/copper-scar-jitx/runs/<attempt>`; exports: `/Users/philippe/dev/copper-scar-jitx/exports/<attempt>`. These paths contain the recorded campaign artifacts and remain local. Do not share a candidate/runtime design name across simultaneous writers. Keep run output outside the candidate project.

Historical scratch: `/private/tmp/copper-scar-jitx-research`; preserve evidence until archived. Runtime installation `/Users/philippe/.jitx/4.4.0` and extension environment `/Users/philippe/.jitx/.venv` are shared machine resources. Coordinate with Main before any install/update/repair; no concurrent global package/runtime mutation. Normal project sessions must use separate project state.

Copperhead owns `/Users/philippe/dev/copper-scar-demo`, branch `codex/demo-takeover`, including its candidates and generated outputs. Do not edit them. Original reference `/Users/philippe/dev/PCBGolf` remains read-only to experiments. Autorouter investigation worktree is separately owned.

The user subsequently authorized committing and pushing the completed JITX checkpoint on codex/jitx-optimization. No merge was requested. Native resets, cleans, deletes and automatic acceptance remain outside this checkpoint. Repository boundaries are collaboration rules, not sandbox guarantees. JITX may use its own native inner-loop checks; benchmark speed AND equivalent coverage before claiming advantage. Independent KiCad checks remain checkpoint/final comparison evidence.

Plan copies: this worktree's `docs/jitx-plan-and-design.md`, external canonical `/Users/philippe/dev/copper-scar-jitx/docs/jitx-plan-and-design.md`, and review `/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/jitx-plan-and-design.md` must remain byte-identical when updated.
